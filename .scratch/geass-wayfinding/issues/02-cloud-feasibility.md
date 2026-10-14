# Verify Google Cloud services and model lifecycle

Type: research
Label: wayfinder:research
Status: resolved
Assignee: cloud_feasibility
Parent: ../map.md
Blocked by: none

## Question

Which PRD cloud capabilities are documented and currently suitable for the chosen demo, particularly BigQuery Graph, ADK deployment, grounding, Model Armor, and Gemini model lifecycle? What readiness gates follow from the evidence?

## Comments

Research asset: [Google Cloud feasibility](../../../docs/research/google-cloud-feasibility.md).

## Answer

Resolved by primary-source documentation research on 2026-10-14. BigQuery Graph exists, but initial SQL projections avoid GQL reservation dependency; search datastore retrieval and public web grounding are distinct. Both PRD Gemini 2.5 models have a documented October 20, 2026 retirement, so model selection is a readiness gate. Model Armor limits and durable stage recovery require explicit application enforcement and tests. The linked research contains source citations and unknowns; no project or API runtime was exercised.
