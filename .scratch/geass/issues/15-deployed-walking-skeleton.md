# 15: Deployed walking skeleton

**What to build:** A publicly reachable URL that answers, backed by a real BigQuery dataset, serving the API and a dark placeholder page — so the whole deploy path is proven before any feature depends on it.

**Blocked by:** wayfinder ticket 05 (*Provision the Google Cloud project*) — a human action this ticket cannot perform

**Status:** ready-for-agent

- [ ] One Cloud Run service is deployed and reachable from outside the builder's network without authentication.
- [ ] The dataset and the SIRUP packages table exist, created by the service's own schema step rather than by hand in a console.
- [ ] A readiness resource reports per-source reachability honestly, including a degraded or unknown state for sources not yet wired.
- [ ] A run or trace resource returns real Cloud Trace spans for the request that produced them.
- [ ] A dark placeholder page renders at the root and identifies the service.
- [ ] A model-call cap and a per-run budget are configured, defaulting to values that cannot exhaust the $300 credit.
- [ ] A money value round-trips from the database through the API as an exact integer IDR value with no floating-point drift.
- [ ] The README states the deployed URL, the project, the region, and where credentials live — with no credential committed to the repository.
