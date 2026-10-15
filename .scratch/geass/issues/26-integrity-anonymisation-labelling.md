# 26: Integrity, anonymisation and labelling pass

**What to build:** A final pass over the deployed artifact that makes the product's claims no larger than its system — the line the spec draws as binding until *Integrity and defamation stance* rules otherwise.

**Blocked by:** 25 (*One-tap dossier*)

**Status:** ready-for-agent

- [ ] A single build flag switches vendor and agency names to anonymised identifiers across every user-visible surface — the radar, the drawer, the graph and generated dossiers.
- [ ] A test proves that with the flag set, no real vendor or agency name appears in any API response or rendered page.
- [ ] Every analytic claim on screen carries its provenance, and no surface presents model-asserted text as computed evidence.
- [ ] Anything stubbed is labelled as such in the interface, reflecting the stub inventory settled by wayfinder ticket 08 (*Architecture lock*).
- [ ] A package whose data could not be grounded, retrieved or classified shows that state honestly rather than defaulting to normal or empty.
- [ ] Address and NPWP clustering is presented as clusters to review and never as a finding of collusion.
- [ ] Any control requiring human approval before publication is visible in the product, and nothing claims human-in-the-loop governance the system does not implement.
- [ ] A unit price above its cap is presented as a delta from a statutory benchmark, with language that leaves room for procurement error rather than intent.
- [ ] The deployed artifact is re-verified after the pass, since earlier slices' tests do not cover a globally flipped rendering flag.
