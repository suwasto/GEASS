# SIRUP public access and bounded capture

Observed **16 October 2026, 23:15–23:19 WIB** using anonymous HTTPS GET requests from this machine. No login, cookies, API credentials, CAPTCHA handling, alternate IP, or access-control workaround was used. Search-tool failures were checked independently with Python's standard HTTP client; a search-tool `402` is not the origin server's status.

## Confirmed route

The [Sukoharjo PPID public-information register](https://ppid.sukoharjokab.go.id/daftar-informasi-berkala/) publishes the [SIRUP D150 recap link](https://sirup.inaproc.id/sirup/rekap/klpd/D150). Its actual public HTML initializes the 2026 recap, which exposes the following read-only UI requests. These are observed application routes, not a documented or stable public API.

1. `GET /sirup/home/rekapitulasi2017?idKldi=D150&levelView=satker&tahunAnggaran=2026`
2. `GET /sirup/datatablectr/datatableruprekapkldi?idKldi=D150&tahun=2026&iDisplayStart=0&iDisplayLength=3&sEcho=1`
3. The first sampled agency is BKPSDM, source satker identifier `351830`. Its public page and loaded fragment identify the provider-list route: `GET /sirup/datatablectr/dataruppenyediasatker?tahun=2026&idSatker=351830&iDisplayStart=0&iDisplayLength=3&sEcho=1`.
4. The list has `aaData` rows `[id_rup, nama_paket, total_pagu, metode, sumber_dana, id_rup, month_label]`. The sampled response advertises 152 records for this agency; only its first three were requested. This is not a regional or national coverage claim.
5. Its rendered links identify `GET /sirup/home/detailPaketPenyediaPublic2017/{id_rup}`. Each of the three sampled detail responses independently contains `Nama KLPD: Kab. Sukoharjo`, `Tahun Anggaran: 2026`, agency, description, volume and exact raw integer pagu. A fourth known RUP identifier, discovered independently from an official non-tender announcement, was verified through the same detail route.

The old `/sirup/home` candidate returned HTTP 404. The global search UI loaded, but its observed search request returned HTTP 200 with an empty body; the importer rejects this as a failed payload, rather than treating it as an empty successful dataset.

## Sample coverage and limits

Four detail records were captured successfully. Descriptions are available in all four. Two specification fields contain meaningful text; two consist only of semicolon separators and are exposed as missing (`null`), with the original response preserved privately. Three volumes are `1 Paket`; the fourth is `0.9 Paket`. None establishes an item-count denominator or a comparable unit price. There is no anomaly classification, markup claim, vendor finding, or completed human review in this dataset.

The fourth record independently confirms the planning identifier, title, agency, year and IDR 90,000,000 pagu of the source-linked transportation feasibility-study procurement. The execution capture owns the non-tender linkage and its evidentiary limits. A shared identifier does not establish payment, delivery or misconduct.

The adapter maps source `Kab. Sukoharjo` to canonical `Kabupaten Sukoharjo` only after an exact scope check. It preserves digit strings, leading zeros and integer IDR amounts without a float conversion. Missing optional fields stay null. A duplicate identifier, unexpected list shape, wrong year/region, missing identity, noninteger monetary field, empty/malformed response or redirect fails the capture. The previous complete snapshot survives a failed recapture.

## Robots, access and reuse

SIRUP `/robots.txt` returned HTTP 404 with an HTML error page. No affirmative automation allowance or redistribution license was established. Public navigation and actual anonymous successful responses establish accessibility of the sampled pages, not unrestricted reuse rights. Keep the source bodies and normalized observations local pending a separate publication decision; no real-case bytes or content are included in parser tests.

LKPP's open-data robots file permits the inspected dataset/download paths while disallowing `/api/`, `/revision/`, `/dataset/rate/` and dataset history. Those disallowed paths were not requested. The [official SIRUP XLSX dataset](https://data.lkpp.go.id/dataset/data-sirup-sistem-informasi-rencana-umum-pengadaan) identifies `prioritas_tahun: 2023` and **No License Provided**. The downloaded 40,720-byte workbook's inspected headers describe aggregate institution RUP values in billions of rupiah and package totals, rather than itemized 2026 planning records. It was not used to seed current packages or prices.

The indexed [Sukoharjo SIAP statistics page](https://siap.sukoharjokab.go.id/ae200c40fd0555ef78557f1444cd4acef549648a/?m=statistik_konstruksi) was checked directly; both its robots file and page refused the connection from this machine. No source bytes or parser were fabricated for that route. The PPID robots file disallows its WordPress administration area, which was not requested.

## Local operation and evidence

From the repository root, after installing the existing runtime dependencies:

```powershell
.venv/Scripts/python.exe -m backend.sources.sirup --max-records 3 --id-rup 67946867
```

This is an operator command, not an anonymous HTTP import endpoint. It uses the verified first agency and explicit year/region scope; it does not crawl all agencies. The default list cap is three, the hard total detail cap is ten (including explicit additional IDs), requests are serial and start at least 1.1 seconds apart, each request times out after 20 seconds, each body is capped at 2 MB, and there are no automatic retries. Recheck portal access conditions before a new capture. The successful bounded four-package run performed five HTTP requests and completed in approximately five seconds; no broader throughput or two-hour abundance result is claimed.

Private outputs under `.local/sources/sirup/`:

- `observations.json`: `{schema_version: 1, records: [...]}`. Every record has its actual detail URL, offset timestamp and SHA-256, exact text fields and nullable missing values. The public observation loader supplies coverage indicators and an unassessed state.
- `<sha256>.bin`: original complete response bytes, matching each recorded digest.
- `latest-import-manifest.json`: list/detail request URL, timestamp, status, byte length and digest for the latest import. This can change on recapture; content hashes may differ because source script attributes change even when package fields do not.
- `capture-manifest.json` and numbered `.bin` files: initial discovery requests, robots responses, HTTP failures and the privately inspected aggregate workbook.

Tests use constructed synthetic HTML/JSON matching the inspected layout. They cover exact IDR above JavaScript's safe-integer range, leading-zero identifiers, optional missing fields, punctuation-only specifications, wrong scope and malformed/login responses, nested tables, duplicate detection, capture bounds and retaining the previous snapshot on failure. No test hits the network.
