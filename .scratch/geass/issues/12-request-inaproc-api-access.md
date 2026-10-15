# Request INAPROC Data Integrator access

Labels: wayfinder:task
Type: task
Status: open
Blocked by: —

Related: 01 established that this access is the difference between a fragile HTML crawl and a supported API over the same data.

## Question

Can the team obtain sanctioned API access to SIRUP data before 18 Oct — and is it worth starting now?

This is a **task**, not a decision. It is a deliberate, low-cost hedge with real option value, and it is **not on the critical path**: the crawl proceeds via the public web UI regardless. It earns its place because approval latency is unknown and the payoff if it lands is large.

*SIRUP retrieval feasibility* found that the INAPROC API Gateway covers exactly the RUP endpoints Module 1 needs, but gates them behind a process:

1. Hold an **INAPROC account**.
2. Apply for the **`Data Integrator`** role. Note the constraint found in the documentation: this role **cannot be applied for** if the account already holds an LPSE procurement-officer role (PP, PPK, Bendahara, and similar).
3. Submit the formal **Surat Permohonan Akses** to LKPP, naming the applicant consistently with their INAPROC account.
4. Await admin approval. The documentation claims approval is *"usually instant for valid LKPP accounts"* and otherwise asks you to allow over 24 hours.
5. In the Developer Portal, generate a JWT token and register the **public IP addresses** that will call the API.
6. Store the token as an environment variable, never in the repository — the repo is public at submission time.

## Answer

Recorded on resolution: whether access was granted, by when, the whitelisted IPs, and where the token is stored. If access did not land, record that too and close — the map does not wait on it.

<!-- appended on resolution -->
