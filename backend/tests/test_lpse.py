"""Offline, invented markup specimens matching the observed public table shape."""
from hashlib import sha256
import json

import pytest

from backend.sources.lpse import LpseClient, LpseSourceError, LpseUnavailable, parse_announcement, parse_idr, parse_participants

URL = "https://spse.inaproc.id/sukoharjokab/nontender/123/pengumumanpl"
PARTICIPANT_URL = "https://spse.inaproc.id/sukoharjokab/nontender/123/peserta"
TIMESTAMP = "2026-10-16T00:00:00+00:00"
ANNOUNCEMENT = """<table class="table table-bordered">
<tr><th>Kode Paket</th><td>123</td></tr>
<tr><th>Nama Paket</th><td>Invented package &amp; checks</td></tr>
<tr><th>Rencana Umum Pengadaan</th><td><table>
<tr><th>Kode RUP</th><th>Nama Paket</th><th>Sumber Dana</th></tr>
<tr><td>456</td><td>Do not override outer title</td><td>APBDP</td></tr>
</table></td></tr>
<tr><th>K/L/PD/Instansi Lainnya</th><td>Kab. Sukoharjo</td></tr>
<tr><th>Satuan Kerja</th><td>Invented agency</td></tr>
<tr><th>Tahun Anggaran</th><td>APBDP 2026</td></tr>
<tr><th>Nilai Pagu Paket</th><td>Rp. 9.007.199.254.740.993,00</td><th>Nilai HPS Paket</th><td>Rp. 9.007.199.254.740.992,99</td></tr>
</table>"""


def test_announcement_exact_money_nested_explicit_rup_and_provenance():
    item = parse_announcement(ANNOUNCEMENT, URL, TIMESTAMP)
    assert item["nama_tender"] == "Invented package & checks"
    assert item["hps"] == "9007199254740992.99"
    assert item["total_pagu"] == "9007199254740993.00"
    assert item["id_rup"] == "456"
    assert item["kind"] == "non_tender"
    assert item["signals"] == []
    assert item["coverage"]["winner"] == "not_observed"
    assert item["provenance"]["synthetic"] is False
    assert item["provenance"]["source_url"] == URL
    assert len(item["provenance"]["sha256"]) == 64


def test_missing_rup_is_not_guessed_from_title():
    html = ANNOUNCEMENT.replace("Kode RUP", "Other identifier")
    item = parse_announcement(html, URL, TIMESTAMP)
    assert item["id_rup"] is None and item["rup_ids"] == []
    assert item["linkage_status"] == "not_linked"


@pytest.mark.parametrize("replacement", ["2025", "2026 2027"])
def test_out_of_scope_or_ambiguous_year_is_rejected(replacement):
    with pytest.raises(LpseSourceError):
        parse_announcement(ANNOUNCEMENT.replace("APBDP 2026", replacement), URL, TIMESTAMP)


@pytest.mark.parametrize("value", ["Rp 1.2.3,00", "Rp 1,000.00", "-12", "NaN", "12e6", ""])
def test_bad_currency_is_not_coerced_to_zero(value):
    with pytest.raises(LpseSourceError):
        parse_idr(value)


def test_identity_mismatch_or_error_page_is_rejected():
    for html in [ANNOUNCEMENT.replace("<td>123</td>", "<td>999</td>"), "<h2>Akses Ditolak!</h2>"]:
        with pytest.raises(LpseSourceError):
            parse_announcement(html, URL, TIMESTAMP)


def test_masked_participant_is_not_a_vendor_identity_or_evaluation():
    html = "<table><thead><tr><th>No</th><th>Nama Peserta</th></tr></thead><tbody><tr><td>1</td><td>Peserta 1</td></tr></tbody></table>"
    result = parse_participants(html, PARTICIPANT_URL, TIMESTAMP)
    participant = result["participants"][0]
    assert participant["identity_status"] == "source_masked"
    assert participant["bid"] is None and participant["evaluation"] is None
    assert participant["alasan_gugur"] is None


def test_fetch_boundary_rejects_non_numeric_ids_before_any_network():
    client = LpseClient()
    with pytest.raises(LpseSourceError):
        client.fetch_public_package("../login")
    assert client._requests == 0


def test_client_budget_stops_before_network():
    client = LpseClient()
    client._requests = 4
    with pytest.raises(LpseUnavailable, match="budget"):
        client._get(URL)


def test_cli_saves_verified_capture_and_retains_snapshot_on_failed_fetch(tmp_path, monkeypatch):
    from backend.sources import lpse

    payload = ANNOUNCEMENT.encode()
    capture = {"url": URL, "retrieved_at": TIMESTAMP, "status": 200,
               "body": payload, "sha256": sha256(payload).hexdigest()}

    class SuccessfulClient:
        captures = [capture]

        def fetch_public_package(self, identifier, kind):
            assert identifier == "123" and kind == "non_tender"
            return parse_announcement(payload, URL, TIMESTAMP)

    private = tmp_path / ".local"
    output = private / "sources" / "lpse"
    monkeypatch.setattr(lpse, "PRIVATE_ROOT", private)
    monkeypatch.setattr(lpse, "LpseClient", SuccessfulClient)
    assert lpse.main(["--id", "123", "--output-dir", str(output)]) == 0
    snapshot_path = output / "observed-execution.json"
    saved = snapshot_path.read_bytes()
    snapshot = json.loads(saved)
    manifest = json.loads((output / snapshot["capture_manifest"]).read_bytes())
    source = manifest["captures"][0]
    assert (output / source["file"]).read_bytes() == payload
    assert source["sha256"] == snapshot["provenance"]["sha256"]

    class FailedClient:
        def fetch_public_package(self, identifier, kind):
            raise LpseUnavailable("SPSE HTTP 403; access stopped without retries")

    monkeypatch.setattr(lpse, "LpseClient", FailedClient)
    with pytest.raises(SystemExit) as error:
        lpse.main(["--id", "123", "--output-dir", str(output)])
    assert error.value.code == 1
    assert snapshot_path.read_bytes() == saved
    assert not list(output.glob("*.tmp"))
