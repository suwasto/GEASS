# Local prototype implementation status

This implementation is a local, offline demonstration of the main investigation flow. All supplied procurement records, benchmark prices, vendors, and relationships are synthetic fixtures. They are not evidence about real procurement or named parties.

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

| Product capability | Local status and limit |
| --- | --- |
| Procurement data | Synthetic examples only; no authenticated or live SIRUP/LPSE retrieval. |
| SSH price grounding | Synthetic benchmark rows demonstrate deterministic comparison; no verified statutory PDF or real regional price claim. |
| Classification and debate | Deterministic fixture behavior; no Gemini call or ADK agent execution. |
| Security screening | Any local demonstration must be labeled local screening; it does not establish Google Model Armor enforcement. |
| Storage | Local process data; BigQuery is not connected or validated. |
| Graph | Synthetic observations and candidate relationships; no beneficial ownership or collusion conclusion. |
| Dossiers | Downloadable drafts only; no submission, email, legal validation, or automatic civic action. |
| Anonymisation | `GEASS_ANONYMIZE=1` before server startup replaces synthetic agency and vendor labels in listing, detail, tender, graph, and dossier responses; verified through HTTP. |
| Runs and traces | Local run/stage records; no Cloud Trace export or Google Cloud telemetry claim. |
| Deployment | Local execution only until separately verified; container configuration is not evidence of a deployed Cloud Run service. |

## Remaining specification gates

Real source permissions and recorded payloads, benchmark applicability and citation verification, real lifecycle joins, model schema and cost controls, Model Armor behavior, BigQuery integration, ADK orchestration, cloud observability, and external deployment remain unverified. No coverage, accuracy, live availability, or competition submission claim follows from passing the offline tests.

The local API filters an exact agency label rather than administrative agency type. Its money fields use decimal strings computed with `Decimal` and explicit two-decimal rounding, rather than the specification's integer-IDR storage contract. There is no retail benchmark fallback, cover-bidding detector across tenders, real vendor identity resolution, durable run storage, or reviewer/publication workflow. Classification labels and counterarguments are curated fixture scenarios; they are not outputs of an implemented prosecutor/defense model loop.
