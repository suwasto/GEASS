# Plan the GEASS evidence-backed hackathon demo

Label: wayfinder:map
Status: resolved

## Destination

Record GEASS architecture choices as ADRs and produce a dependency-ordered build plan that can be sliced into implementation tickets. Stop before production code, provisioning, deployment, or implementation tickets.

## Notes

- Source: [GEASS PRD](../../geass_prd_master_implementation_plan.md). Baseline is a repository containing only the PRD; no app, deployment configuration, or tracker setup existed.
- Local Markdown tracker for this effort; this is not a switch of the repository's GitHub tracker. Each decision child lives under `issues/`, with `Type`, `Label`, `Status`, `Assignee`, `Parent`, and `Blocked by`. Use statuses `open`, `claimed`, `resolved`; a resolved prerequisite unblocks a child. Empty assignee means unclaimed. Append answers as resolution comments under `## Answer`; preserve the original question.
- Frontier query: scan child files in numeric order for open, unassigned tickets whose blockers are resolved. Research workers are allowed by the invoked wayfinder workflow. Research assets remain local; no research branch, push, or external issue is needed for this planning-only effort.
- Consult wayfinder, grilling, domain-modeling, and research. One human decision ticket spans the architecture boundary rounds; research tickets may resolve in the same session. No further human decision ticket is resolved here.
- The user's standing-decision placeholder is not a stack instruction. Actual choices are recorded in the human decision answer and ADRs.
- [Build plan](../../docs/geass-build-plan.md) describes delivery order and acceptance gates. It is not a set of implementation tickets.

## Decisions so far

- [Set the GEASS demo architecture and publication boundary](issues/01-demo-operating-boundary.md): user-selected demo scope, Cloud Run web stack, resumable batches, review and evidence tradeoffs; six ADRs and a sequenced build plan record the route.
- [Verify Google Cloud services and model lifecycle](issues/02-cloud-feasibility.md): SQL graph projections first; current model lifecycle, grounding distinctions and screening/durability limits become readiness gates.
- [Verify procurement data assumptions and threshold rules](issues/03-public-data-feasibility.md): source coverage remains sample-gated, execution links preserve provenance, and threshold rules depend on category and effective regulation.

## Not yet specified

None of the initial-demo architecture questions need to remain vague: known prerequisites belong in the build plan's readiness gate. New questions discovered by sampling or provisioning should reopen this map or create a precisely named child before implementation depends on them.

## Out of scope

Production code, implementation ticket creation, provisioning, spending, deployment, external publication, nationwide operation, autonomous accusations, and civic-message sending. Extended PRD modules remain later milestones, not hidden initial-demo commitments.
