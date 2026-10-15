# 25: One-tap dossier

**What to build:** A flagged case turned into a document a journalist or auditor can actually send, in one action.

**Blocked by:** 19 (*SSH grounding and the implied unit price*), 22 (*Syndicate graph for one tender*), 24 (*Bounded adversarial loop*)

**Status:** ready-for-agent

- [ ] One action on a flagged package produces a draft **Surat Permohonan Informasi Publik** under UU No. 14/2008 requesting the underlying documents for that `id_rup`.
- [ ] One action produces an **APIP/BPK** risk brief covering the package, its markup delta in IDR, the linked tender where one exists, and any vendor-graph anomalies.
- [ ] Every generated document is phrased as a request for information and contains no assertion that any person or company did anything wrong.
- [ ] A test asserts that no generated document contains an assertion of wrongdoing, and would fail if one were introduced.
- [ ] Each claim in a dossier carries its provenance, so a recipient can trace a figure back to its source and its regulation.
- [ ] A dossier for a package with an ungrounded price states that the price could not be grounded rather than omitting the section quietly.
- [ ] The surviving defense rebuttal is included wherever the adversarial loop ran.
- [ ] Generation is a single request that returns a rendered, downloadable document rather than a partial stream.
