---
status: accepted
date: 2026-10-16
---
# Carry the current prototype into the live-data wave

The owner requested implementation of the newer upstream prototype specification and then authorized the live-data-to-deployment plan. The implementation uses one FastAPI service with HTML/CSS/JavaScript. Keep that working interface for the next wave rather than introducing a frontend migration. This supersedes the React/Vite part of ADR 0002 for the current prototype; Google Cloud remains the delivery target.

Public source observations are facts with provenance and explicit missing-field coverage. They are not approved risk findings. Source capture or a model result cannot authorize publication of a risk finding. Preserve exact-version human review, private source objects, counterevidence and withdrawal for real-case publication, as required by ADR 0003. The synthetic fixture workflow is a separate software demonstration and cannot supply live evidence or a review decision.

Source availability and project credentials must be verified through actual requests. Failed access is recorded as unavailable; it must not silently switch to a synthetic success. Paid cloud work remains gated on the owner-provided project, spending authorization and limits. Operator access is not a public API capability.

BigQuery is the intended canonical analytical store. Local capture files support development and reproducibility only; they do not establish that the cloud storage milestone is complete. Keep the decimal-string HTTP contract and deterministic arithmetic while the live storage schema is verified.
