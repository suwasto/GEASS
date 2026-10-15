# 24: Bounded adversarial loop

**What to build:** A prosecutor-versus-defense review that can remove a finding before a user ever sees it, and that cannot run away with the budget.

**Blocked by:** 18 (*Gemini normalisation and the taxonomy*); wayfinder ticket 08 (*Architecture lock*), which owns the stop condition

**Status:** ready-for-agent

- [ ] Before an accusatory-shaped signal survives, a defense pass searches for a legitimate explanation and can remove or downgrade the finding.
- [ ] The loop enforces a hard stop condition on turns and tokens rather than advising one, and a run that hits it fails loudly.
- [ ] The defense's rebuttal is retained and shown beside a surviving finding, so a signal arrives with its counter-argument attached.
- [ ] A finding removed by the defense is absent from every user-visible surface, including the listing, the drawer and generated dossiers.
- [ ] The outcome distinguishes "the defense found a valid exception" from "the defense found nothing", so a thin defense cannot silently clear a finding.
- [ ] The loop's cost per run is recorded and visible in the telemetry panel.
- [ ] A bounded run's behaviour at the limit is covered by a test, including that it does not exceed the configured cap.
