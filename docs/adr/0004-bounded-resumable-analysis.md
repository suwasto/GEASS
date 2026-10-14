---
status: accepted
date: 2026-10-14
---
# Analyze in bounded resumable batches

The user selected a manually triggered, resumable batch pipeline with precomputed results rather than live autonomous monitoring. Source revision, package identity, analysis version, and selected model identify a work item; persist each completed stage and retry only incomplete or failed stages. Re-running a work item must not duplicate findings or erase a human review.

Use explicit state transitions and bounded ADK steps, not an unconstrained agent loop. Configure limits for selected packages, model calls, wall time, and retries before running. Browser reads never trigger analysis. Failed or unavailable dependencies produce a visible incomplete result rather than silently falling back to an unsupported classification.
