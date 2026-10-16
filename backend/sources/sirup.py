"""Bounded public SIRUP capture for one verified Sukoharjo agency; no model output."""
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import argparse
import json
from pathlib import Path
import re
import time
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

BASE = "https://sirup.inaproc.id"
LIST_URL = BASE + "/sirup/datatablectr/dataruppenyediasatker?tahun=2026&idSatker=351830&iDisplayStart=0&iDisplayLength={limit}&sEcho=1"
DETAIL_PATH = "/sirup/home/detailPaketPenyediaPublic2017/"
MAX_BYTES = 2_000_000


class SourceError(ValueError):
    """A failed response is evidence of failure, never an empty successful dataset."""


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SourceError("Source redirected the request; inspect the public route before continuing")


urlopen = build_opener(_NoRedirect()).open


class _DetailTable(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.fields = {}
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1
        if tag == "tr":
            self.rows.append([])
        elif tag in {"td", "th"} and self.rows:
            self.rows[-1].append({"text": [], "label": "label-left" in dict(attrs).get("class", "").split()})
        elif tag == "br" and self.rows and self.rows[-1]:
            self.rows[-1][-1]["text"].append(" ")

    def handle_data(self, text):
        if not self.hidden and self.rows and self.rows[-1]:
            self.rows[-1][-1]["text"].append(text)

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)
        if tag == "tr" and self.rows:
            cells = self.rows.pop()
            if len(cells) == 2 and cells[0]["label"]:
                label, value = (" ".join("".join(cell["text"]).split()) for cell in cells)
                if label in self.fields:
                    raise SourceError(f"Duplicate detail label: {label}")
                self.fields[label] = value or None


def _body(payload):
    if not payload or len(payload) > MAX_BYTES:
        raise SourceError("Empty or oversized source response")
    try:
        return payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise SourceError("Source is not UTF-8") from error


def parse_list(payload: bytes, limit: int = 3):
    if not 1 <= limit <= 10:
        raise SourceError("Record cap must be between 1 and 10")
    try:
        data = json.loads(_body(payload))
    except json.JSONDecodeError as error:
        raise SourceError("Malformed list response or login HTML") from error
    if not isinstance(data, dict) or not isinstance(data.get("aaData"), list):
        raise SourceError("Missing aaData list")
    rows = data["aaData"]
    if not rows or len(rows) > limit:
        raise SourceError("Empty list or server ignored requested record cap")
    ids = []
    for row in rows:
        if not isinstance(row, list) or len(row) != 7 or not isinstance(row[0], str) or not re.fullmatch(r"[0-9]{1,20}", row[0]):
            raise SourceError("Unexpected package list row")
        if row[0] in ids:
            raise SourceError("Duplicate package identifier")
        ids.append(row[0])
    return ids


def parse_detail(payload: bytes, source_url: str, retrieved_at: str):
    parsed = urlparse(source_url)
    if parsed.scheme != "https" or parsed.netloc != "sirup.inaproc.id" or not re.fullmatch(DETAIL_PATH + r"[0-9]{1,20}", parsed.path) or parsed.query or parsed.fragment:
        raise SourceError("Unsupported public detail locator")
    try:
        timestamp = datetime.fromisoformat(retrieved_at)
        if timestamp.utcoffset() is None:
            raise ValueError("missing timezone")
    except (ValueError, TypeError) as error:
        raise SourceError("Retrieval timestamp needs an explicit timezone") from error
    parser = _DetailTable()
    parser.feed(_body(payload))
    fields = parser.fields
    identifier = fields.get("Kode RUP")
    if identifier != parsed.path.rsplit("/", 1)[1]:
        raise SourceError("Missing or mismatched package identifier")
    for label in ["Nama Paket", "Satuan Kerja", "Tahun Anggaran", "Nama KLPD"]:
        if not fields.get(label):
            raise SourceError(f"Missing required source field: {label}")
    if fields["Tahun Anggaran"] != "2026" or fields["Nama KLPD"] != "Kab. Sukoharjo":
        raise SourceError("Source is outside verified Sukoharjo 2026 scope")
    pagu = fields.get("Total Pagu")
    if pagu is not None and not re.fullmatch(r"[0-9]+", pagu):
        raise SourceError("Pagu must be an exact integer IDR string; no inferred locale conversion")
    mapping = {"description": "Uraian Pekerjaan", "spesifikasi_pekerjaan": "Spesifikasi Pekerjaan",
               "volume_pekerjaan": "Volume Pekerjaan", "metode_pemilihan": "Metode Pemilihan"}
    record = {"id_rup": identifier, "nama_paket": fields["Nama Paket"], "satker": fields["Satuan Kerja"],
              "region": "Kabupaten Sukoharjo", "tahun_anggaran": 2026, "total_pagu": pagu,
              **{key: fields.get(label) for key, label in mapping.items()}, "source_url": source_url,
              "retrieved_at": retrieved_at, "source_sha256": sha256(payload).hexdigest()}
    for key in mapping:
        if record[key] is not None and not any(character.isalnum() for character in record[key]):
            record[key] = None
    return record


def capture(output_dir: Path, limit: int = 3, extra_ids=()):
    """Operator-invoked only. Fixed official routes, serial requests, no retries or credentials."""
    if not 1 <= limit <= 10:
        raise SourceError("Record cap must be between 1 and 10")
    if any(not re.fullmatch(r"[0-9]{1,20}", identifier) for identifier in extra_ids):
        raise SourceError("Explicit package identifiers must contain only digits")
    if len(extra_ids) + limit > 10:
        raise SourceError("Total list/detail capture cap is 10 packages")
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    last_request = 0.0

    def fetch(url):
        nonlocal last_request
        delay = 1.1 - (time.monotonic() - last_request)
        if delay > 0:
            time.sleep(delay)
        last_request = time.monotonic()
        observed = datetime.now(timezone.utc).isoformat()
        request = Request(url, headers={"User-Agent": "GEASS-Source-Research/0.1 (bounded public procurement review)"})
        with urlopen(request, timeout=20) as response:
            if response.status != 200 or response.url != url:
                raise SourceError("Non-200 response or redirect; capture stopped")
            payload = response.read(MAX_BYTES + 1)
            _body(payload)
            digest = sha256(payload).hexdigest()
            (output_dir / f"{digest}.bin").write_bytes(payload)
            manifest.append({"source_url": url, "retrieved_at": observed, "sha256": digest,
                             "bytes": len(payload), "status": response.status, "redistributed": False})
        return payload, observed

    try:
        list_url = LIST_URL.format(limit=limit)
        raw_list, list_time = fetch(list_url)
        ids = parse_list(raw_list, limit)
        manifest[-1]["coverage"] = {"list_rows": len(ids), "scope": "one agency, year 2026"}
        ids = list(dict.fromkeys(ids + list(extra_ids)))
        records = []
        for identifier in ids:
            url = BASE + DETAIL_PATH + identifier
            body, observed = fetch(url)
            record = parse_detail(body, url, observed)
            records.append(record)
            manifest[-1]["coverage"] = {key: record[key] is not None for key in (
                "total_pagu", "description", "spesifikasi_pekerjaan", "volume_pekerjaan", "metode_pemilihan")}
        snapshot = {"schema_version": 1, "records": records}
        # A failed recapture must leave the previous complete snapshot intact.
        temporary = output_dir / "observations.json.tmp"
        temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(output_dir / "observations.json")
        return snapshot
    finally:
        (output_dir / "latest-import-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--output-dir", type=Path, default=Path(".local/sources/sirup"))
    command.add_argument("--max-records", type=int, default=3)
    command.add_argument("--id-rup", action="append", default=[], help="Additional known public package ID within the total cap of 10")
    options = command.parse_args()
    snapshot = capture(options.output_dir, options.max_records, options.id_rup)
    print(json.dumps({"records": len(snapshot["records"]), "snapshot": str(options.output_dir / "observations.json")}))
