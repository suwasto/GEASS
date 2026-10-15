# Provision the Google Cloud project

Labels: wayfinder:task
Type: task
Status: open
Blocked by: —
Blocks: 08, 09, 10

Related: 04 tells this ticket which APIs to enable.

## Question

Nothing exists on Google Cloud, and only a human can create it. What exactly has to be done, and is it done?

This is a **task**, not a decision: its job is to unblock the *Architecture lock* ticket and everything downstream. It is **HITL** — the agent cannot create a billing account, accept terms, or authenticate on the human's behalf, and there is no `gcloud` CLI on this machine today.

## Checklist

1. Create or select a GCP project. Record the project id and your chosen region.
2. Attach billing, and confirm what credits or free-trial balance the account actually has (see *Google Cloud stack verification* for what to expect).
3. Enable the APIs the architecture needs — the exact list depends on that ticket's verdict, but expect: Cloud Run, Artifact Registry, Cloud Build, Vertex AI, BigQuery, and whichever security and search products survive verification.
4. Install the `gcloud` CLI on this machine. It is currently **missing**, which blocks every deployment path.
5. Authenticate: either `gcloud auth application-default login` for local development, or a service-account key written somewhere the project can read. Do **not** commit it — the eventual repo is public.
6. Prove it end to end: deploy a hello-world container to Cloud Run and confirm it answers on a public URL.
7. Record where credentials live, so later tickets can find them without guessing.

## Answer

Recorded on resolution: project id, region, enabled APIs, credential location, whether a Cloud Run deploy has succeeded, and the available credit balance. Every downstream ticket depends on these facts, so they are recorded precisely rather than described.

<!-- appended on resolution -->
