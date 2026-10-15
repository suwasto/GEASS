# Radar and forensic drawer

Labels: wayfinder:prototype
Type: prototype
Status: open
Blocked by: 06, 07, 08

Related: realises the surfaces that 07 scripts and 08 prices.

## Question

What do the two surfaces actually look and behave like — and does the density the PRD wants survive contact with a real screen and a three-minute video?

This is a **prototype** ticket: the point is a cheap, rough, concrete artifact to react to, not a finished interface. UX and Solution Design are only 10% of the rubric, but they are also the entire surface a judge sees, so the shape must be settled before it is built properly.

Two surfaces:

**The radar** — a high-density table of `ID RUP`, `NAMA PAKET`, `PEMILIK`, `SATKER / LOKASI`, `PAGU (IDR)`, `KLASIFIKASI AI`, and `ALASAN & BENCHMARK HARGA`, with filters by region, agency type, and anomaly class.

- What columns earn their width when the video is watched at 720p on someone else's laptop?
- How do the classification badges read at a glance — `ABSURD`, `INDICATED MARKUP`, `SPECIFICATION LOCK`, `SPLIT PACKAGE`, `NORMAL`?
- The PRD asks for a dark-mode, glowing-badge aesthetic. Is that legible, or does it obscure the data the entry is being judged on?
- Filter affordances: how does a judge see that millions of rows are behind this?

**The forensic drawer** — price and SSH forensics, the syndicate graph, and the dossier action, opening from a row click.

- What is the price-forensics block: implied unit price versus SSH cap versus retail, and how is the delta shown in IDR so it lands in one second?
- Where does the prosecutor-versus-defense reasoning appear, and how much of it is legible on video?
- The graph: rendered as a static image, a simple node-link layout, or genuinely interactive — given the architecture ticket will have priced interactivity already?
- The one-tap dossier button and what visibly happens when it is pressed.

## Deliverable

A rough, running artifact to react to — a static page or minimal app is enough. The PRD's own prose reserved the name **"Enrich with AHU Deed"** for a feature already ruled out of scope; the drawer should not reserve space for it.

<!-- appended on resolution -->
