"""Bounded, TLS-verified public SPSE observation; no inference or vendor enrichment.

Captured source bytes stay private. Publishing observations needs a separate reuse basis.
"""
import argparse
from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import time
from uuid import uuid4
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.robotparser import RobotFileParser

BASE_URL = "https://spse.inaproc.id/sukoharjokab"
USER_AGENT = "GEASS-Research/0.1 (bounded public procurement observation; no authentication)"
MAX_BYTES = 2_000_000
PRIVATE_ROOT = Path(__file__).resolve().parents[2] / ".local"
PATH = re.compile(r"/sukoharjokab/(lelang|nontender)/(\d{1,20})/(pengumumanlelang|pengumumanpl|peserta)$")


class LpseSourceError(ValueError):
    """The source cannot support a valid observation."""


class LpseUnavailable(RuntimeError):
    """A source rejected access or could not be reached. Do not retry around it."""


class _Node:
    def __init__(self, tag="", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return " ".join(" ".join(child if isinstance(child, str) else child.text()
                                for child in self.children).split())

    def find(self, tag):
        for child in self.children:
            if isinstance(child, _Node):
                if child.tag == tag:
                    yield child
                yield from child.find(tag)


class _Document(HTMLParser):
    def __init__(self, payload):
        super().__init__(convert_charrefs=True)
        if len(payload) > MAX_BYTES:
            raise LpseSourceError("Source document exceeds the observation size limit")
        self.root = _Node()
        self.stack = [self.root]
        try:
            self.feed(payload.decode("utf-8") if isinstance(payload, bytes) else payload)
        except (UnicodeError, RecursionError) as exc:
            raise LpseSourceError("Malformed source document") from exc

    def handle_starttag(self, tag, attrs):
        node = _Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            if len(self.stack) >= 100:
                raise LpseSourceError("Source HTML nesting exceeds the observation limit")
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def _rows(table):
    """Ignore nested tables when reading a table's own rows."""
    for child in table.children:
        if isinstance(child, _Node):
            if child.tag == "tr":
                yield [cell for cell in child.children if isinstance(cell, _Node) and cell.tag in {"th", "td"}]
            elif child.tag in {"thead", "tbody", "tfoot"}:
                yield from _rows(child)


def parse_idr(value):
    """Parse the observed Indonesian currency display without a float conversion."""
    value = re.sub(r"^Rp\.?\s*", "", value.strip(), flags=re.I)
    if not re.fullmatch(r"(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d{1,2})?", value):
        raise LpseSourceError("Malformed IDR amount; refusing guessed arithmetic")
    return format(Decimal(value.replace(".", "").replace(",", ".")), "f")


def _source(payload, source_url, retrieved_at, stage):
    parsed = urlsplit(source_url)
    if parsed.scheme != "https" or parsed.netloc != "spse.inaproc.id" or not PATH.fullmatch(parsed.path) or parsed.query or parsed.fragment:
        raise LpseSourceError("Expected a canonical public Sukoharjo SPSE URL")
    raw = payload.encode("utf-8") if isinstance(payload, str) else payload
    return {"stage": stage, "source_url": source_url, "retrieved_at": retrieved_at,
            "sha256": sha256(raw).hexdigest(), "synthetic": False,
            "computed": False, "model_asserted": False,
            "reuse_status": "private_observation_only; public_redistribution_not_cleared"}


def parse_announcement(payload, source_url, retrieved_at):
    """Read an announcement and only its explicit RUP row(s); no title matching."""
    provenance = _source(payload, source_url, retrieved_at, "public_spse_announcement")
    path = PATH.fullmatch(urlsplit(source_url).path)
    kind, identifier, section = path.groups()
    if section != ("pengumumanlelang" if kind == "lelang" else "pengumumanpl"):
        raise LpseSourceError("URL is not an announcement")
    tables = list(_Document(payload).root.find("table"))
    table = next((table for table in tables if "table-bordered" in table.attrs.get("class", "").split()), None)
    if table is None:
        raise LpseSourceError("Announcement table missing; no empty success is recorded")
    fields, rup_ids = {}, []
    for cells in _rows(table):
        for index in range(0, len(cells) - 1, 2):
            header, value = cells[index], cells[index + 1]
            if header.tag != "th" or value.tag != "td":
                continue
            key = header.text()
            fields[key] = value.text()
            if key == "Rencana Umum Pengadaan":
                for nested in value.find("table"):
                    nested_rows = list(_rows(nested))
                    if not nested_rows:
                        continue
                    headings = [cell.text() for cell in nested_rows[0]]
                    if "Kode RUP" not in headings:
                        continue
                    column = headings.index("Kode RUP")
                    for row in nested_rows[1:]:
                        if column >= len(row) or not re.fullmatch(r"\d{1,20}", row[column].text()):
                            raise LpseSourceError("Malformed explicit RUP identifier")
                        rup_ids.append(row[column].text())
    code = fields.get("Kode Tender", fields.get("Kode Paket"))
    title = fields.get("Nama Tender", fields.get("Nama Paket"))
    years = re.findall(r"\b20\d{2}\b", fields.get("Tahun Anggaran", ""))
    if code != identifier or not title or years != ["2026"] or fields.get("K/L/PD/Instansi Lainnya") != "Kab. Sukoharjo":
        raise LpseSourceError("Announcement identity, jurisdiction, or 2026 scope mismatch")
    try:
        hps, pagu = parse_idr(fields["Nilai HPS Paket"]), parse_idr(fields["Nilai Pagu Paket"])
        agency = fields["Satuan Kerja"]
    except KeyError as exc:
        raise LpseSourceError("Required announcement field missing") from exc
    rup_ids = list(dict.fromkeys(rup_ids))
    return {"id": identifier, "kode_lelang": identifier,
            "kind": "tender" if kind == "lelang" else "non_tender",
            "nama_tender": title, "satker": agency, "region": "Kab. Sukoharjo",
            "tahun_anggaran": 2026, "total_pagu": pagu, "hps": hps,
            "id_rup": rup_ids[0] if len(rup_ids) == 1 else None, "rup_ids": rup_ids,
            "linkage_status": "explicit_source_rup" if rup_ids else "not_linked",
            "stage": fields.get("Tahap Tender Saat Ini", fields.get("Tahap Paket Saat Ini")),
            "participants": [], "signals": [], "nama_pemenang": None,
            "coverage": {"announcement": "observed", "participants": "not_fetched",
                         "evaluations": "not_observed", "winner": "not_observed"},
            "synthetic": False, "provenance": provenance}


def parse_participants(payload, source_url, retrieved_at):
    provenance = _source(payload, source_url, retrieved_at, "public_spse_participants")
    if not urlsplit(source_url).path.endswith("/peserta"):
        raise LpseSourceError("URL is not a participant section")
    for table in _Document(payload).root.find("table"):
        rows = list(_rows(table))
        if not rows or [cell.text() for cell in rows[0]] != ["No", "Nama Peserta"]:
            continue
        participants = []
        for row in rows[1:]:
            if len(row) != 2 or not row[0].text().isdigit() or not row[1].text():
                raise LpseSourceError("Malformed participant row")
            name = row[1].text()
            participants.append({"id": "source-row-" + row[0].text(), "nama_peserta": name,
                                 "identity_status": "source_masked" if re.fullmatch(r"Peserta\s+\d+", name, re.I) or "*" in name else "public_name_only",
                                 "bid": None, "evaluation": None, "alasan_gugur": None,
                                 "bid_to_hps_percent": None})
        return {"participants": participants, "provenance": provenance}
    raise LpseSourceError("Observed participant table missing or changed")


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise LpseUnavailable("SPSE redirected the request; inspect it manually before continuing")


class LpseClient:
    """At most four requests per instance, with no retries or access bypasses."""
    def __init__(self):
        self.captures = []
        self._requests, self._last_request = 0, 0.0
        self._delay = 1.1
        self._opener = build_opener(_NoRedirect())
        self._robots = None

    def _get(self, url):
        if self._requests >= 4:
            raise LpseUnavailable("Public observation request budget exhausted")
        time.sleep(max(0, self._delay - (time.monotonic() - self._last_request)))
        self._requests += 1
        self._last_request = time.monotonic()
        try:
            with self._opener.open(Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,text/plain"}), timeout=20) as response:
                if response.status != 200:
                    raise LpseUnavailable("SPSE returned a non-success response")
                body = response.read(MAX_BYTES + 1)
                if len(body) > MAX_BYTES:
                    raise LpseSourceError("Source response exceeds the observation size limit")
                retrieved_at = datetime.now(timezone.utc).isoformat()
                capture = {"url": url, "retrieved_at": retrieved_at, "status": response.status,
                           "sha256": sha256(body).hexdigest(), "body": body}
                self.captures.append(capture)
                return body, retrieved_at
        except HTTPError as exc:
            raise LpseUnavailable(f"SPSE HTTP {exc.code}; access stopped without retries") from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise LpseUnavailable("SPSE could not be reached with verified TLS") from exc

    def fetch_public_package(self, identifier, kind="non_tender"):
        if not isinstance(identifier, str) or not re.fullmatch(r"\d{1,20}", identifier) or kind not in {"tender", "non_tender"}:
            raise LpseSourceError("Expected a numeric package ID and explicit procurement kind")
        if self._robots is None:
            body, _ = self._get("https://spse.inaproc.id/robots.txt")
            if not body.lstrip().startswith(b"# Robots"):
                raise LpseUnavailable("Source robots policy could not be verified")
            self._robots = RobotFileParser()
            self._robots.parse(body.decode("utf-8").splitlines())
            self._delay = max(self._delay, self._robots.crawl_delay(USER_AGENT) or 0)
        path = "lelang" if kind == "tender" else "nontender"
        announcement = "pengumumanlelang" if kind == "tender" else "pengumumanpl"
        url = f"{BASE_URL}/{path}/{identifier}/{announcement}"
        participant_url = f"{BASE_URL}/{path}/{identifier}/peserta"
        if not self._robots.can_fetch(USER_AGENT, url) or not self._robots.can_fetch(USER_AGENT, participant_url):
            raise LpseUnavailable("Source robots policy excludes this public path")
        body, timestamp = self._get(url)
        record = parse_announcement(body, url, timestamp)
        try:
            body, timestamp = self._get(participant_url)
            participants = parse_participants(body, participant_url, timestamp)
            record["participants"] = participants["participants"]
            record["participant_provenance"] = participants["provenance"]
            record["coverage"]["participants"] = "observed"
        except (LpseUnavailable, LpseSourceError) as exc:
            record["coverage"]["participants"] = "unavailable"
            record["participant_error"] = str(exc)
        return record


def _atomic_write(path, content):
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Privately observe one public Sukoharjo 2026 SPSE package; no bulk retrieval.")
    parser.add_argument("--id", required=True, help="Known numeric public package identifier")
    parser.add_argument("--kind", choices=["non_tender", "tender"], default="non_tender")
    parser.add_argument("--output-dir", type=Path, default=PRIVATE_ROOT / "sources" / "lpse")
    args = parser.parse_args(argv)
    output = args.output_dir.resolve()
    if not output.is_relative_to(PRIVATE_ROOT.resolve()):
        parser.error("Source captures must stay inside the repository's ignored .local directory")
    client = LpseClient()
    try:
        record = client.fetch_public_package(args.id, args.kind)
        if record["coverage"]["participants"] == "unavailable":
            raise LpseUnavailable("Participant observation failed; retaining the previous execution snapshot")
        output.mkdir(parents=True, exist_ok=True)
        manifest = {"captured_at": datetime.now(timezone.utc).isoformat(), "captures": []}
        for capture in client.captures:
            body = capture["body"]
            digest = sha256(body).hexdigest()
            if digest != capture["sha256"]:
                raise LpseSourceError("Capture digest mismatch; retaining the previous snapshot")
            filename = digest + ".bin"
            _atomic_write(output / filename, body)
            manifest["captures"].append({key: value for key, value in capture.items() if key != "body"} | {"file": filename, "bytes": len(body)})
        # A unique manifest keeps an older snapshot's references valid after a failed write.
        manifest_name = "manifest-" + uuid4().hex + ".json"
        _atomic_write(output / manifest_name, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"))
        record["capture_manifest"] = manifest_name
        _atomic_write(output / "observed-execution.json", json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8"))
    except (LpseSourceError, LpseUnavailable, OSError) as exc:
        parser.exit(1, f"Observation failed; previous snapshot retained: {exc}\n")
    print(f"Saved private {record['kind']} observation {record['id']} with {len(client.captures)} source captures to {output}")
    return 0


if __name__ == "__main__":
    main()
