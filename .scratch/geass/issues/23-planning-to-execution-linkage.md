# 23: Planning↔execution linkage

**What to build:** An honest answer, on screen, to whether a flagged planning package can be tied to the tender that executed it — and the product behaving truthfully whichever way the answer falls.

**Blocked by:** 21 (*LPSE execution view*); wayfinder ticket 13 (*Does id_rup join to kode_lelang?*), which holds the answer

**Status:** ready-for-agent

- [ ] If a published join exists, the flagged package and its downstream tender are linked by it, and the drawer presents the planning anomaly and the execution view as one connected case.
- [ ] If only a heuristic is available, the drawer labels it as a heuristic and states exactly what it matched on.
- [ ] If no join exists, the product says plainly that it has none and presents the two sides side by side without implying a connection it cannot evidence.
- [ ] The heuristic case reports its own reliability on the real cases it was tested against, rather than asserting that it works.
- [ ] Whichever outcome holds, no surface of the product claims lifecycle tracking the system cannot demonstrate.
- [ ] The linkage state is part of the package detail payload, so the frontend never infers it.
- [ ] All three outcomes are covered by tests, so the honest path cannot silently degrade into an overclaim.
