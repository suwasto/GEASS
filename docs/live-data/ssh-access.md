# Sukoharjo 2026 SSH: observed source and extraction

Verified 16 October 2026. This is a real source specimen, not a synthetic fixture. It has not been matched to a real procurement package or approved as a comparison for one.

## Official source and capture

The [official JDIH detail](https://jdih.sukoharjokab.go.id/produk/detail/14646) currently lists Peraturan Bupati Sukoharjo Nomor 2 Tahun 2026, *Standar Harga Satuan Tahun Anggaran 2026*, as **Berlaku**, with enactment/publication date 27 January 2026. The live **Download** link leads to [the official Sukodrive PDF](https://sukodrive.sukoharjokab.go.id/s/oiMEKJ7n8ztfyFT/download).

The old `/file/dokumen/...2026-ooqqd.pdf` URL cited in earlier research returned 403 through the web reader. That does not mean the current source is inaccessible: an ordinary unauthenticated GET of the current Download link succeeded. No authentication or access-control workaround was used. Only one source PDF was downloaded; no broad crawl occurred.

| Capture field | Observed value |
| --- | --- |
| HTTP method | GET |
| Source URL | `https://sukodrive.sukoharjokab.go.id/s/oiMEKJ7n8ztfyFT/download` |
| Capture completion, local file modification timestamp | `2026-10-16T16:15:20.784133+00:00` |
| Exact bytes | 5,912,168 |
| SHA-256 | `3910ac030e98c1779fd6ead55bddb135e25ba3372140e8d083956dd394aba3a6` |
| PDF page count | 371 |
| Private raw file | `.local/sources/ssh/perbup-2-2026.pdf` |
| Private provenance/candidate manifest | `.local/sources/ssh/manifest.json` |
| Access basis | Public official legal-information download; no login presented |
| Redistribution status | Not assessed; raw file, full extracted text, and rendered images stay in ignored `.local/` |

The timestamp above is the downloaded file's modification timestamp, not a publisher-supplied retrieval field. HTTP response headers were not retained and an ETag or source revision is not claimed. The document hash identifies the captured revision.

## Text layer and manually checked rows

The downloaded PDF has a usable native text layer: `pypdf` extracted 2,601 characters and 37 complete row candidates from physical PDF page 7. Physical page 7 is also printed page 7, Lampiran I, **Standar Satuan Harga**. Local rendering with `pypdfium2` was visually inspected against the extracted text. No OCR or LLM extraction was needed.

These three rows were checked visually on that page. All share account code `5.1.02.01.001.00001`. Group/item numbers are separate printed subcolumns; they are not invented globally unique item identifiers.

| PDF/printed page | Group / item | Description as printed | Unit as printed | Listed IDR price |
| --- | --- | --- | --- | ---: |
| 7 / 7 | 1 / 4 | Aspal padat (drum) | Kg | 21,000 |
| 7 / 7 | 2 / 2 | Semen Portland 40 kg | zak | 63,000 |
| 7 / 7 | 3 / 1 | Kaca Bening tb.3 mm | m2 | 92,000 |

These are **candidate rows requiring applicability review**, not automatic statutory maximums for every purchase. A price for a `zak` of 40 kg must not be treated as a per-kg price; item specification and unit remain part of the match. The parser preserves the printed unit and converts only the unambiguous Indonesian thousands-separated integer price.

## Legal applicability and limits

The captured operative pages distinguish planning from execution:

- PDF page 3, Pasal 2(1)–(2), describes use in planning and execution and a planning upper-bound role.
- PDF page 4, Pasal 2(3), distinguishes execution ceilings from prices that may be exceeded in specified conditions, including market increases. Pasal 2(5) states tax inclusion. Pasal 2(6) assigns the four annexes.
- PDF page 4, Pasal 3, addresses changed or unlisted prices/items, electronic catalogues and other official prices, and price-selection considerations. PDF page 5, Pasal 4, describes a change process.

Physical page 4 was also rendered and visually checked. These provisions make a blanket “above this row means unlawful spending” claim invalid. A package-specific comparison still needs fiscal year, jurisdiction, exact item/specification, quantity, tax/logistics treatment, applicable amendments or approved changes, and the planning/execution context. The official catalogue status was observed, but a complete search for subsequent amendments was not performed. This is source examination, not legal certification.

## Implemented extraction and checks

`backend/sources/ssh.py` contains an offline parser for conservative, complete single-line rows and an explicitly selected-page PDF extraction helper. The helper requires `pypdf`; the bundled workspace Python already supplies it. No application dependency or requirements file was changed. The parser never promotes candidates to applicable benchmarks and never changes the public synthetic corpus.

Three synthetic parser tests pass with:

```powershell
.\.venv\Scripts\python.exe -m unittest backend.tests.test_ssh -v
```

They verify exact integer prices and preserved units/specifications; abstention on headers, broken multiline rows, malformed grouping, negative or zero prices; and required page/source provenance. The actual captured page was also extracted through `extract_pdf_candidates` with `pages=[7]` using the bundled Python runtime. Other pages, irregular/multiline table layouts, OCR-only material, and nationwide coverage are not validated.
