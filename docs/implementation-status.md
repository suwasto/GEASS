# Local prototype implementation status

The original demonstration remains synthetic. A subsequent source wave adds separate, locally captured public Sukoharjo 2026 observations and operator-run retrieval. Source facts are unassessed and are not findings about wrongdoing. Raw captures are ignored by Git and are not shipped in the container.

The controlling product specification is `.scratch/geass/spec.md` on `origin/main`. This status file records the narrower implementation and does not amend that specification.

## Scope and verification

The local flow is: filter the radar, inspect a package and its price provenance, follow an explicitly linked synthetic tender, inspect participant relationships, and download a draft request or risk brief. The same service provides the page and HTTP JSON API. Seven synthetic packages cover the five classification labels, a bundled-volume abstention, and a mismatched-year benchmark abstention.

On 16 October 2026, the combined suite passed **17 tests** (7 focused backend checks and 10 independent HTTP acceptance checks) in 2.72 seconds:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The suite launches real local HTTP servers and checks filtered/paginated listing, exact price arithmetic, bundle and incompatible-benchmark abstention, explicit missing lifecycle links, participant identity and graph edge consistency, downloadable synthetic draft dossiers, provenance, bounded/invalid parameters, fixture-run retrieval, refusal of live execution, degraded source health, and the anonymisation flag across all public record payloads. It uses Python's standard library and makes no requests to procurement or cloud services.

The HTTP checks cover structured behavior, not statutory accuracy, classifier accuracy, legal suitability, source reachability, or production security. A missing or incompatible benchmark cannot produce an effective NORMAL classification; that case is not assessed and is excluded from the NORMAL filter.

Browser verification against the running local service covered populated radar, pagination, empty search, package investigation, exact displayed comparison, bundled-quantity abstention, wrong-year abstention displaying Not assessed, tender participants, graph and equivalent relationship table, successful PPID and audit downloads, and actual local fixture-run spans. The initial blank-filter validation error was fixed before the final check. A 390-pixel viewport rendered without document horizontal overflow; the viewport was reset afterward. The final browser error log was empty. JavaScript syntax checks passed. Screenshots are local verification artifacts under ignored `.local/`.

Docker configuration was written but the container build and Cloud Run deployment were not executed. Full assistive-technology validation and exhaustive browser/error recovery automation were not performed.

## Explicit service inventory

### Public-source wave (16 October 2026)

- Four genuine SIRUP details were captured anonymously, with source URL, retrieval time and exact SHA-256. Descriptions are present in all four; meaningful specifications in two. Three volumes are `1 Paket`, one is `0.9 Paket`; none supplies a defensible item denominator.
- One public **non-tender** SPSE announcement explicitly identifies RUP `67946867`. The planning record independently matches the agency, jurisdiction and year. The public participant is masked; bids, evaluations, rejection reasons and winner are unavailable. A checked tender returned HTTP 403 and access stopped.
- The official 371-page Sukoharjo SSH PDF was captured privately. Native text extraction works; three page-7 row candidates were visually checked. They remain unapproved candidates and are not matched to these planning packages.
- The local app can load operator-selected planning/execution snapshots, select public observations versus synthetic fixtures, inspect provenance and source links, and render the explicit source relationship graph. Real dossiers and analysis are disabled. External clients cannot read real captures; source reuse/publication is not yet cleared.
- The snapshot loaders reject malformed source identities, unsupported scope, nonfinite money, unobserved risk assertions and mismatched execution provenance. Offline parser/HTTP checks cover failures and preservation of earlier complete captures. The expanded suite passes **61 tests**; the only warning is an upstream test-client deprecation. No live service is called by that suite.

The live local browser was checked with the configured four-record snapshot: all four planning ceilings display exactly; no record shows an invented classification or price delta; the RUP `67946867` investigation shows the explicit non-tender relation, masked participant, unknown bid/evaluation/winner, exact HPS, source graph/table, source link/hash and Asia/Jakarta capture time. Real dossier links are absent. The synthetic dataset remains separately selectable. Source capture commands were run against real public endpoints independently of the offline suite.

Reproducible capture/start commands are in [README](../README.md). Exact access findings and limits are in [SIRUP](live-data/sirup-access.md), [SSH](live-data/ssh-access.md) and [LPSE](live-data/lpse-access.md). These current observations supersede the older broad feasibility verdicts; they do not establish national coverage or full tender forensics.

| Product capability | Local status and limit |
| --- | --- |
| Procurement data | Bounded operator-run public SIRUP/SPSE capture works locally; source facts and synthetic fixtures are separate. No authenticated API access or bulk crawl. |
| SSH price grounding | Official source PDF and native-text candidate parser verified; no applicable package comparison approved. Synthetic comparisons remain software demonstrations. |
| Classification and debate | Deterministic fixture behavior; no Gemini call or ADK agent execution. |
| Security screening | Any local demonstration must be labeled local screening; it does not establish Google Model Armor enforcement. |
| Storage | Private local snapshots plus process data; BigQuery is not connected or validated. |
| Graph | One explicit planning-to-non-tender relation and masked source participant, plus separate synthetic graph; no beneficial ownership or collusion conclusion. |
| Dossiers | Downloadable drafts only; no submission, email, legal validation, or automatic civic action. |
| Anonymisation | `GEASS_ANONYMIZE=1` before server startup replaces synthetic agency and vendor labels in listing, detail, tender, graph, and dossier responses; verified through HTTP. |
| Runs and traces | Local run/stage records; no Cloud Trace export or Google Cloud telemetry claim. |
| Deployment | Local execution only until separately verified; container configuration is not evidence of a deployed Cloud Run service. |

## Remaining specification gates

Public redistribution/reuse basis, an applicable package benchmark, full tender/evaluation coverage, model schema and cost controls, Model Armor behavior, BigQuery integration, ADK orchestration, cloud observability, and external deployment remain open. An explicit non-tender join is verified locally; it does not complete the full tender lifecycle gate. No accuracy, continuous availability, or competition submission claim follows from passing the offline tests.

The local API filters an exact agency label rather than administrative agency type. Its money fields use decimal strings computed with `Decimal` and explicit two-decimal rounding, rather than the specification's integer-IDR storage contract. There is no retail benchmark fallback, cover-bidding detector across tenders, real vendor identity resolution, durable run storage, or reviewer/publication workflow. Classification labels and counterarguments are curated fixture scenarios; they are not outputs of an implemented prosecutor/defense model loop.
