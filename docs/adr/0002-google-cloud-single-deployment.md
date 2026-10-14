---
status: accepted
date: 2026-10-14
---
# Keep the Google Cloud backend and serve the web demo in one deployment

The user fixed the PRD's Google Cloud backend and selected React/TypeScript with Vite, served by Python/FastAPI on Cloud Run. Google ADK orchestrates bounded analysis, Vertex AI supplies model inference, and BigQuery holds analytical data. A single web/API deployment avoids separate frontend hosting and cross-origin configuration during the demo.

Use Cloud Storage for immutable source captures and dossier artifacts, and Firestore for mutable run checkpoints and review state. BigQuery remains the analytical store rather than the operational job queue. This is a planning recommendation derived from the chosen resumable batch and publication boundaries; verify regional compatibility and provision costs before implementation.

Run manually triggered analysis in a Cloud Run Job rather than holding a browser request open. The public service reads completed results; a restricted operator surface triggers jobs and reviews findings. Model identifiers are selected at the readiness gate instead of hardcoding the PRD's Gemini 2.5 identifiers.
