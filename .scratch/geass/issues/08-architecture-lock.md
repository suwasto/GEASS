# Architecture lock

Labels: wayfinder:grilling
Type: grilling
Status: open
Blocked by: 04, 05

## Question

Given only what the stack verification proved actually exists, what is the concrete system — how many agents, running where, with what boundary between the model and deterministic SQL — and what is stubbed versus real?

This is the ticket that turns the PRD's diagram into something buildable. The PRD's diagram is aspirational; several of its boxes may not survive ticket 04, and nothing can run until ticket 05 produces a project.

Decisions this ticket settles:

- **Agent topology.** Five ADK agents as the PRD specifies, or one service with staged prompts? Judges read the repo, so the answer has to be defensible as architecture rather than as a diagram that flatters the PRD.
- **The neuro-symbolic split.** The PRD's best line is "the AI never does raw math": Gemini extracts and classifies, BigQuery SQL computes. Pin down exactly which computations are deterministic and which are model claims, because this is the claim a technical judge will probe hardest.
- **What BigQuery actually does.** Validating, storing, or graph traversal only. If "BigQuery Graph" did not survive verification, name the substitute and describe what the graph is actually built from.
- **Grounding path.** Vertex AI Search over SSH PDFs, a pre-extracted table, or live web grounding — whichever the JDIH ticket proved workable, and no more.
- **The adversarial loop.** In or out, now that its cost is visible. If in, define the stop condition so it cannot run away with the token budget.
- **Deployment topology.** What runs on Cloud Run, what is static, and how the browser reaches it.
- **Stub inventory.** An explicit list of what is faked for the demo and how it is labelled, so no one accidentally claims a stub is a system on stage.

## Answer

A component list with the model/SQL boundary drawn explicitly, the deployment topology, and the stub inventory.

<!-- appended on resolution -->
