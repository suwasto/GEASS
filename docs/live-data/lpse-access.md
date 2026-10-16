# LPSE public-source feasibility — Sukoharjo, 2026

Checked **16 October 2026, Asia/Jakarta**. Direct HTTPS observations used verified TLS, an identifying research user agent, bounded response sizes and at least 1.1 seconds between government requests. All source bytes and captures are private under `.local/sources/lpse/`, which is ignored by Git. No authentication, CAPTCHA solving, access bypass, paid service or bulk crawl was used.

## Verdict

**Amber for public non-tender announcement coverage; not established for tender execution.** A real 2026 public non-tender announcement carries an explicit RUP identifier. Its public participant page exposes a masked row only. A checked tender announcement rejected access with HTTP 403. This is sufficient for a local planning-to-**non-tender** observation, not for a tender winner, bid comparison, evaluation finding or vendor syndicate graph.

The prior research ticket's broad green verdict is not supported by this narrower live check. A library documenting a field does not establish that a selected public portal exposes that field today.

## Official access policy and reuse boundary

The canonical host is [SPSE Sukoharjo](https://spse.inaproc.id/sukoharjokab), confirmed both by its canonical link and the maintained PyProc host metadata. The official [robots policy](https://spse.inaproc.id/robots.txt) permits `/`, explicitly lists `/sukoharjokab`, and specifies `Crawl-delay: 1`. It excludes `/api/redirect`; no call was made to that path.

The official [SPSE terms](https://spse.inaproc.id/sukoharjokab/publik/syaratketentuan), section E.2, include:

> Pengguna dilarang dengan cara apapun memanfaatkan, memperbanyak, atau berperan dalam penjualan/menyebarkan setiap data dan informasi ... untuk kepentingan pribadi dan/atau komersial.

The ellipsis omits the clause describing information obtained from the application. Section E.1 separately restricts copying or modifying the application's source code without written permission. The adapter does not copy the application's JavaScript or redistribute captured HTML.

**Interpretation, not a legal conclusion:** robots permits limited automated retrieval, while the terms raise a separate question about the purpose and redistribution of retrieved data. These checks do not establish an open-data reuse license or a blanket prohibition on public-interest observation. This implementation therefore keeps records local and marks their reuse status as uncleared. Establish the basis for public-oversight use and redistribution before deploying real SPSE records publicly. Do not infer that the third-party PyProc code license licenses government records.

Terms response: HTTP 200, captured `2026-10-16T16:16:45.589956+00:00`; SHA-256 `4ebe228bc5b6ead91675b0cadc79260f849928c2526536cd65f2815e45db0f95`.

## Direct observations

| Public source | Observed result | Coverage consequence |
| --- | --- | --- |
| [Sukoharjo home](https://spse.inaproc.id/sukoharjokab) | HTTP 200; announcement links include non-tender packages | A discoverable public non-tender record exists; the home page is not an annual tender census. |
| [Tender search](https://spse.inaproc.id/sukoharjokab/lelang) | HTTP 200; the page's normal public search form points to a 2026 DataTables POST | The bounded public request returned `data: []` and `recordsTotal: 2147483647`; that total is not a credible procurement count. Record listing coverage as unavailable, not zero tenders. |
| [Tender announcement 10152180000](https://spse.inaproc.id/sukoharjokab/lelang/10152180000/pengumumanlelang) | HTTP 403, “Akses Ditolak!” | Access stopped. No retry, alternate identity, session manipulation or hidden route was attempted. The identifier was a discovery lead; its tender facts were not adopted from an unofficial site. |
| [Non-tender announcement 11082329000](https://spse.inaproc.id/sukoharjokab/nontender/11082329000/pengumumanpl) | HTTP 200, jurisdiction Kab. Sukoharjo and budget year APBDP 2026; nested `Rencana Umum Pengadaan` table contains `Kode RUP` **67946867** | A directly published cross-reference exists for this non-tender record. The parser does not join by title or amount. This observation alone does not establish broad tender linkage. |
| [Non-tender participants](https://spse.inaproc.id/sukoharjokab/nontender/11082329000/peserta) | HTTP 200, one source-labelled `Peserta 1` row; the observed table has only `No` and `Nama Peserta` columns | Identity is masked. No NPWP, address, bid, evaluation, rejection reason or winner is supplied by this table. A participant row number is not a reusable vendor identity. |

Only the non-tender announcement and participants were parsed into the private execution snapshot. No document attachment was downloaded. The announcement's present stage is not contract completion; no winner was inferred from it.

### Evidence manifest

| Capture | Retrieved at, UTC | SHA-256 |
| --- | --- | --- |
| `spse-robots.body` | `2026-10-16T16:15:43.947349+00:00` | `65c8595c5c9df059c115f9cbaf026ccb4f903a8d8320ab195c31e760c220809a` |
| `spse-sukoharjo.body` | `2026-10-16T16:16:18.295366+00:00` | `ae01314a5e31456a82d074552ef5bc0e713b1cf0cda9f9d9a010d59be8c3b615` |
| `tender-list-data.body` | `2026-10-16T16:17:27.063097+00:00` | `b65fe586f3ae6e67f51d9c5eebf2d9a7085a9d584f255b96e4d2cff5162d3262` |
| `tender-announcement.body` | `2026-10-16T16:17:57.754839+00:00` | `738c8aa21bbbe3f9ff64f362930622b611e9ffcc1ed2485cf2c45d6cc15ccc8c` |
| `nontender-announcement.body` | `2026-10-16T16:17:47.620552+00:00` | `90e59f79bf969e16d2a5bb9dc0f622cf8d3d67cdffa0339d0bbbb0611f57fc8c` |
| `nontender-participants.body` | `2026-10-16T16:18:24.560027+00:00` | `4b34d595f947e9bbf36ff8681b5bbc2952be3cad5ebbfdbcf3ca7db26c81e5d6` |

Each capture has a sibling `.meta.json` containing its URL, status and retrieval timestamp. Session headers in private research captures must not be published. The safe local integration object is `.local/sources/lpse/observed-execution.json`; it contains no NPWP or address and no identified vendor.

## PyProc verification and adapter decision

[PyPI's release metadata](https://pypi.org/pypi/pyproc/json) reports **PyProc 0.3.3**, uploaded **11 June 2026**. Its wheel SHA-256 is `74646a66c24bea409ebfaf5cbb47ee1830c2ea5fe42c017a8a7cdf3542ee1001`; the downloaded wheel matched that digest. It was inspected without installation. [GitHub repository metadata](https://api.github.com/repos/wakataw/pyproc) reports an unarchived repository, with [master commit `3a2b1d9`](https://github.com/wakataw/pyproc/commit/3a2b1d992b68abd501b6ee7303963303aeb5d2e4) dated **25 June 2026**. Those are maintenance signals, not a promise that a current live portal works.

Inspection of both the release wheel and [upstream `lpse.py`](https://github.com/wakataw/pyproc/blob/3a2b1d992b68abd501b6ee7303963303aeb5d2e4/pyproc/lpse.py) found:

- The announcement parser already reads `rencana_umum_pengadaan` through `parse_rup`. The earlier ticket's uncertainty based on README tool names missed this implementation.
- `parse_currency` returns a Python float. Its output cannot serve GEASS's exact evidentiary money boundary.
- The package-list POST explicitly passes `verify=False`, irrespective of a client initialized with verification enabled. GEASS must preserve verified TLS.
- The library's Python interface and MCP interface have different request-lifecycle responsibilities. The README's MCP rate limit is not evidence that a custom Python caller automatically receives it.

**Decision:** no PyProc dependency was added. The small, replaceable adapter in `backend/sources/lpse.py` parses only the public table shape directly observed here, using the standard library and exact decimal strings. This deviation from the original library preference avoids silently adopting float money, disabled TLS or undocumented coverage. Re-evaluate a pinned version after those requirements are met; never wrap floats back into strings and call the result exact.

## Adapter contract and checks

`parse_announcement(payload, source_url, retrieved_at)` returns the source ID, explicit procurement `kind`, title, agency, jurisdiction, year, exact decimal-string `total_pagu` and `hps`, explicit `rup_ids`, optional single `id_rup`, source stage, coverage and provenance. Multiple explicit RUP rows remain a list; the parser does not select one arbitrarily. Missing RUP rows produce `not_linked`.

`parse_participants(...)` handles the observed two-column public table. Masked names are marked `source_masked`; bids, evaluations, rejection reasons and bid-to-HPS ratios remain null. It does not enrich identities, derive associations or infer a winner.

`LpseClient.fetch_public_package(identifier, kind="non_tender")` checks robots and requests only the canonical announcement and participant pages. It has a four-request lifetime budget, one-second minimum spacing, verified default TLS, a response-size bound, numeric-ID validation, no redirects and no retries. A non-200, malformed or out-of-scope announcement fails visibly. A participant failure preserves the valid announcement with explicit unavailable participant coverage. Source captures are exposed only to the caller, which must persist them privately.

Fifteen offline tests in `backend/tests/test_lpse.py` check exact values beyond JavaScript's safe integer range, malformed currencies, nested RUP tables, absent linkage, source identity/year mismatch, access-error HTML, participant masking, request bounds, and the operator refresh preserving a previous snapshot after a failed fetch. Test markup is invented, not copied government HTML. The actual private announcement and participant capture also parse successfully with their recorded digests. Live fetching is intentionally excluded from automated tests.

### Reproduce the private observation

From the repository root, using the project's Python environment:

```powershell
.venv/Scripts/python.exe -m backend.sources.lpse --id 11082329000 --kind non_tender
```

This exact operator command was successfully exercised against the public source after the parser tests. It defaults to `.local/sources/lpse/`; `--output-dir` may select another directory only inside this repository's ignored `.local/` tree. It requests robots, announcement and participant pages, then writes content-addressed `<sha256>.bin` source bodies and a unique capture manifest. The manifest's URL, retrieval time, status, digest and byte count are linked from `observed-execution.json`. It never stores session headers in the integration snapshot or manifest.

The snapshot is replaced atomically only after every requested observation and capture write succeeds. A blocked, unreachable or malformed refresh leaves the previous snapshot intact and exits unsuccessfully. A valid announcement with an unavailable participant section can be inspected through the Python interface, but the operator command refuses to overwrite a previous snapshot with that partial refresh. This operator tool does not connect the public API to a background crawler.

Unverified: public evaluation/winner coverage, a public 2026 **tender** announcement, bid-to-HPS comparisons, masked-NPWP resolution, repeated co-bidding, shared-address groups and a public redistribution basis. None is claimed by this adapter.
