# GEASS

Government Expenditure Anomaly & Syndicate Surveillance: an evidence workspace for procurement review.

The application supports **captured public observations** and a separate **synthetic demonstration**. Real Sukoharjo 2026 planning records can be captured locally with the bounded importers below. The demonstration dataset exercises price comparisons, tender relationships and draft dossiers; its labels are not real findings.

## Run locally (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8080
```

Open [GEASS locally](http://127.0.0.1:8080). There is no frontend build or separate frontend service.

## Capture public records locally

These operator commands use fixed, observed official routes, verified TLS, bounded requests and polite spacing. They do not require credentials. Access can change; a failed refresh preserves the previous complete snapshot. Raw captures remain under ignored `.local/`; they are not redistributed with the code.

```powershell
.\.venv\Scripts\python.exe -m backend.sources.sirup --max-records 3 --id-rup 67946867
.\.venv\Scripts\python.exe -m backend.sources.lpse --id 11082329000 --kind non_tender
$env:GEASS_OBSERVATIONS = '.local/sources/sirup/observations.json'
$env:GEASS_EXECUTION = '.local/sources/lpse/observed-execution.json'
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8080 --no-proxy-headers
```

When configured, the page opens the captured-observation dataset. The source selector switches to the separate synthetic demo. Source facts have no risk classification, price delta or dossier until supporting evidence and review exist. The verified example links a planning record to **non-tender** procurement; it does not show bid evaluations or a winner. Bundled `1 Paket` / `0.9 Paket` quantities do not establish comparable item counts.

Real captures are currently served only to loopback clients. External access is denied until source reuse and authenticated publication are implemented; forwarded headers cannot opt into this access. Keep the local server bound to `127.0.0.1` and use the command above without proxy-header trust. The container contains no private captures.

See [SIRUP access](docs/live-data/sirup-access.md), [SSH source inspection](docs/live-data/ssh-access.md), and [LPSE coverage and terms](docs/live-data/lpse-access.md). Optional selected-page PDF extraction uses `requirements-source.txt`; native-text candidate extraction does not establish legal applicability or a package match.

## What works

- Filtered, paginated procurement radar with exact IDR amounts.
- Investigation details with source coverage, supporting evidence and counterevidence.
- Deterministic price comparisons that abstain when quantities or benchmarks cannot be compared.
- Tender participants and a rendered relationship graph with a table alternative; candidate relationships do not establish ownership or collusion.
- Downloadable PPID information-request and APIP/BPK brief drafts, with evidence limits.
- Bounded local fixture execution and an inspector that distinguishes local stages from unavailable cloud integrations.

Fixture records are not real source captures. Browsing does not refresh external sources or trigger paid inference. There is no working reviewer authentication/publication workflow yet; real observations remain local and unassessed. No anonymous import or approval endpoint accepts external records. Demo dossier downloads remain synthetic only.

## Implementation baseline

The repository was already cloned from [suwasto/GEASS](https://github.com/suwasto/GEASS). Implementation follows the newer prototype specification in upstream commit `907a9955cbfa5495b06a66493a396f099a9e1977` (`.scratch/geass/spec.md`), using one FastAPI service and a lightweight HTML/JavaScript frontend. That newer specification differs from the earlier React/Vite ADR; the existing decision documents remain intact for traceability.

The initial local implementation does **not** complete the live-data, cloud or competition submission acceptance gates. See [implementation status](docs/implementation-status.md) for the feature and integration inventory.

The [next-wave plan](docs/next-wave-plan.md) sequences live source retrieval, grounding, protected analysis, review and Cloud Run deployment with completion evidence for each step.

## Container

```powershell
docker build -t geass .
docker run --rm -p 8080:8080 geass
```

The container serves the same fixture application. A container recipe is not evidence of a Cloud Run deployment. Cloud project selection, authorized billing, credentials, real source captures and integration checks remain prerequisites for cloud delivery. Never put service-account credentials in this repository or in browser assets.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
node --check backend/static/app.js
```

API and calculation checks run without live sources or model calls. Commands and observed results are recorded in [implementation status](docs/implementation-status.md).

The original [PRD](geass_prd_master_implementation_plan.md), [domain glossary](GLOSSARY.md), [build plan](docs/geass-build-plan.md) and [design references](docs/design/README.md) provide project context. A planning ceiling is not actual spending; a risk signal is not a verdict.
