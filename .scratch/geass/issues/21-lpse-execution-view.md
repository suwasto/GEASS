# 21: LPSE execution view

**What to build:** What happened to a package after planning — who bid, who was disqualified, why, and who won — retrieved through a maintained library and rendered on the row a user is already looking at.

**Blocked by:** 17 (*Per-package detail crawl*)

**Status:** ready-for-agent

- [ ] Tender announcement, participants, evaluations, `alasan_gugur`, winner and schedule retrieved for a set of real tenders.
- [ ] Retrieval goes through the maintained library, pinned to an exact version and wrapped behind a thin internal boundary so it can be replaced or vendored.
- [ ] Both a nationwide host and per-institution host resolution work, so tenders are reachable across separately operated regional portals.
- [ ] `nilai_hps` and each `harga_penawaran` are stored as exact IDR values, and bid-to-HPS is computed deterministically.
- [ ] The execution view opens from a radar row and lists each participant with its evaluation outcome, disqualification reason and bid value, alongside the winner.
- [ ] Disqualification text is displayed verbatim beside any analysis of it, so a reader can judge the text themselves.
- [ ] A tender that cannot be retrieved is reported as unavailable for that package rather than rendering an empty view.
- [ ] Retrieval and the execution view are covered by tests over the recorded specimens with no network access.
