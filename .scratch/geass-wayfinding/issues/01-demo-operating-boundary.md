# Set the GEASS demo architecture and publication boundary

Type: grilling
Label: wayfinder:grilling
Status: resolved
Assignee: Codex with user
Parent: ../map.md
Blocked by: none

## Question

What scope, stack, execution model, publication boundary, and evidence tradeoffs should govern the first GEASS build so it can be planned without silently assuming the user's priorities?

## Comments

### Architecture round 1 — user answers

- Focused hackathon demo; nationwide ingestion and public uploads later.
- Google Cloud backend fixed; frontend initially undecided.
- Human review before publication; public risk signals and evidence; reviewer actions/uploads require login.

### Architecture round 2 — user answers

- React/TypeScript with Vite served by FastAPI on Cloud Run.
- Region/year selected by validated SIRUP → LPSE → SSH sample; no immediate Sukoharjo commitment.
- Manually triggered, resumable bounded batch pipeline with cached investigation results; budget/deadline are inputs before provisioning.

### Architecture round 3 — user answer

The user accepted SQL vendor evidence edges, exact source lifecycle links, evidence abstention, Markdown draft dossiers, and explicit later milestones for GQL reservations, enrichment, geocoding, retail benchmarks, uploads, and PDF output.

## Answer

Resolved with the user on 2026-10-14 after three architecture rounds. The accepted boundary is recorded in [ADRs](../../../docs/adr/) and developed into the [sequenced build plan](../../../docs/geass-build-plan.md). The implementation must select region/year through captured evidence and establish budget, project access, supported model and deadline before paid execution. Those are entry gates, not invented standing decisions. Only this one human decision ticket was resolved in the session.
