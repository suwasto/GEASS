"""Conservative candidates from native-text SSH rows; never automatic legal grounding."""

from pathlib import Path
import re


ROW = re.compile(
    r"^(?P<account>\d+(?:\.\d+){5})\s+(?P<group>\d+)\s+(?P<item>\d+)\s+"
    r"(?P<description>.+?)\s+(?P<unit>[^\s]+)\s+"
    r"(?P<price>\d{1,3}(?:\.\d{3})+|\d+)\s*$"
)


def parse_page_candidates(text: str, *, pdf_page: int, source_id: str) -> list[dict]:
    """Return complete single-line table rows, preserving printed units and item text."""
    if pdf_page < 1 or not source_id.strip():
        raise ValueError("A one-based PDF page and source identifier are required")
    rows = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = ROW.fullmatch(line.strip())
        if match is None:
            continue
        fields = match.groupdict()
        price = int(fields["price"].replace(".", ""))
        if price <= 0:
            continue
        rows.append({
            "kode_rekening": fields["account"], "group_code": fields["group"],
            "item_code": fields["item"], "uraian": fields["description"],
            "satuan": fields["unit"], "listed_price_idr": price,
            "pdf_page": pdf_page, "text_line": line_number, "source_id": source_id,
            "raw_row": line.strip(), "applicability_status": "candidate_requires_review",
        })
    # shortcut: multiline or irregular PDF rows are omitted; use layout extraction and human review before broader coverage.
    return rows


def extract_pdf_candidates(path: str | Path, *, pages: list[int], source_id: str) -> dict:
    """Read explicitly selected pages; caller owns source capture and approval."""
    from pypdf import PdfReader

    if not pages or any(not isinstance(page, int) or isinstance(page, bool) or page < 1 for page in pages):
        raise ValueError("Select at least one valid one-based PDF page")
    reader = PdfReader(path)
    if any(page > len(reader.pages) for page in pages):
        raise ValueError("Selected page exceeds PDF length")
    rows, coverage = [], []
    for page_number in sorted(set(pages)):
        text = reader.pages[page_number - 1].extract_text() or ""
        page_rows = parse_page_candidates(text, pdf_page=page_number, source_id=source_id)
        rows.extend(page_rows)
        coverage.append({"pdf_page": page_number, "text_characters": len(text), "candidate_rows": len(page_rows)})
    return {"page_count": len(reader.pages), "coverage": coverage, "candidates": rows,
            "limitation": "Native text candidates only; OCR and legal/comparability approval are not performed."}
