import json

import pytest

from backend.sources.sirup import SourceError, parse_detail, parse_list

URL = "https://sirup.inaproc.id/sirup/home/detailPaketPenyediaPublic2017/000123"
WHEN = "2026-10-16T16:17:30+00:00"


def specimen(**changes):
    # Synthetic content, preserving only the inspected public table structure.
    fields = {"Kode RUP": "000123", "Nama Paket": "Paket &amp; contoh", "Nama KLPD": "Kab. Sukoharjo",
              "Satuan Kerja": "Instansi sintetis", "Tahun Anggaran": "2026", "Volume Pekerjaan": "1 Paket",
              "Total Pagu": "9007199254740993", "Uraian Pekerjaan": "Kertas", "Spesifikasi Pekerjaan": "",
              "Metode Pemilihan": "E-Purchasing"}
    fields.update(changes)
    rows = "".join(f'<tr><td class="label-left">{key}</td><td>{value}</td></tr>' for key, value in fields.items())
    return f'<div><table>{rows}</table></div>'.encode()


def test_exact_money_identifier_missing_values_and_source_hash():
    row = parse_detail(specimen(), URL, WHEN)
    assert row["id_rup"] == "000123" and row["total_pagu"] == "9007199254740993"
    assert row["spesifikasi_pekerjaan"] is None
    assert row["region"] == "Kabupaten Sukoharjo"
    assert row["nama_paket"] == "Paket & contoh" and row["volume_pekerjaan"] == "1 Paket"
    assert len(row["source_sha256"]) == 64 and row["retrieved_at"] == WHEN
    assert parse_detail(specimen(**{"Spesifikasi Pekerjaan": "; ; ;"}), URL, WHEN)["spesifikasi_pekerjaan"] is None


@pytest.mark.parametrize("changes", [{"Kode RUP": "456"}, {"Tahun Anggaran": "2025"},
                                     {"Nama KLPD": "Kab. Lain"}, {"Total Pagu": "NaN"},
                                     {"Total Pagu": "9.000.000"}, {"Satuan Kerja": ""}])
def test_unverifiable_or_malformed_detail_fails(changes):
    with pytest.raises(SourceError):
        parse_detail(specimen(**changes), URL, WHEN)


def test_login_and_empty_response_are_not_empty_success():
    for payload in [b"", b"<html>Login</html>", b'{"data": []}']:
        with pytest.raises(SourceError):
            parse_list(payload)
        with pytest.raises(SourceError):
            parse_detail(payload, URL, WHEN)


def test_list_cap_duplicate_and_nested_table_handling():
    row = ["000123", "Paket contoh", "900", "Metode", "APBD", "000123", "January 2026"]
    assert parse_list(json.dumps({"aaData": [row]}).encode()) == ["000123"]
    with pytest.raises(SourceError):
        parse_list(json.dumps({"aaData": [row, row]}).encode())
    nested = '<table><tr><td class="label-left">Lokasi</td><td><table><tr><td>X</td><td>Y</td></tr></table></td></tr></table>'
    assert parse_detail(nested.encode() + specimen(), URL, WHEN)["total_pagu"] == "9007199254740993"


def test_timestamp_and_locator_must_be_verifiable():
    for url, timestamp in [(URL, "2026-10-16"), (URL.replace("sirup.inaproc.id", "example.org"), WHEN)]:
        with pytest.raises(SourceError):
            parse_detail(specimen(), url, timestamp)


def test_reimport_is_bounded_and_failure_preserves_complete_snapshot(tmp_path, monkeypatch):
    from backend.sources import sirup

    row = ["000123", "Paket contoh", "900", "Metode", "APBD", "000123", "January 2026"]
    calls = []
    broken = False

    class Response:
        status = 200

        def __init__(self, request):
            self.url = request.full_url

        def __enter__(self):
            return self

        def __exit__(self, *_):
            pass

        def read(self, _):
            if "datatablectr" in self.url:
                return json.dumps({"aaData": [row]}).encode()
            return b"<html>Login</html>" if broken else specimen()

    def fetch(request, timeout):
        calls.append(request.full_url)
        assert timeout == 20
        return Response(request)

    monkeypatch.setattr(sirup, "urlopen", fetch)
    monkeypatch.setattr(sirup.time, "sleep", lambda _: None)
    for _ in range(2):
        assert len(sirup.capture(tmp_path, 1)["records"]) == 1
    previous = (tmp_path / "observations.json").read_bytes()
    broken = True
    with pytest.raises(SourceError):
        sirup.capture(tmp_path, 1)
    assert (tmp_path / "observations.json").read_bytes() == previous
    assert len(calls) == 6
