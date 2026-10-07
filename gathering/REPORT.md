# Gathering 05

2026-10-07: read tools before execution. All 15 offline commands and all 14
live line commands passed. Exact commands, exits and output are in
check-results.json. Public read-only RPC/Sourcify; Python standard library,
`-B` throughout; no line files changed. These are local observations.

| Line | Tried / works | Broken / remaining limits |
| --- | --- | --- |
| 1 | Health, agreement, sampling and new progress demos plus all four live commands. Providers agreed at 26137137; three 13-second-spaced progress samples observed advances without anomalies. | No reproduced regression. Short-window freshness/progress does not establish uptime or provider independence. |
| 2 | Preview checks, revert-name self-test, typed preparation tests and encode-only demo; all three live previews. ZTO balance decoded 0; transfer named InsufficientBalance with balance 0, needed 1. | Prior unsized-integer documentation defect fixed. Preparation explicitly says previewed=false. Arrays/tuples excluded; latest-state calls are not future transaction guarantees. |
| 3 | Route, authority, delegate scan, clone context and new UUPS self-tests; all five live ZTO scans at 26137137. 1287 code bytes; recognized slots empty; no watched opcodes or exact clone; ending hashes matched. | No reproduced regression in exercised cases. Positive clone/UUPS paths remain synthetic; UUID responses cannot prove authorization. Metadata separation is heuristic; custom routers remain unresolved. |
| 4 | Source and trailer self-tests plus both live ZTO commands. Source unverified; solc 0.8.26 trailer without metadata hash. Identity mismatch regression now rejected, including missing/wrong chain/address and malformed identity types. | Prior source-identity defect fixed. No verified ZTO source or independent compilation. Compiler trailer is only a hint; source provider availability and malformed responses remain external dependencies. |

Each line serves unfamiliar workers outside the cave. Their goals are distinct:
endpoint reliability, call outcomes, upgrade reconnaissance, source review.
Supporting ABI and block evidence does not duplicate another line's goal.
For 21 Pepes, keep line 1 to bounded reliability observations; line 2 to bounded
ABI call outcomes; line 3 to named proxy patterns and observable candidates;
line 4 to source bundles and compiler context. Narrow any promise of universal
uptime, future execution, complete upgrade authorization or universal rebuilds
to those scopes.

Shared: copied RPC Progress and UUPS Probe, refreshed Typed Preview and Compiler
Trailer from repaired originals, with source hashes in shared/provenance.json.
New uups_sources.py joins line 3 candidate addresses to line 4 source review.
It deduplicates candidates, skips empty implementations, preserves lookup
failures and distinguishes current source reports from pinned chain evidence.

All six shared integration checks and four copied-tool offline demonstrations
passed. Both live shared commands passed: UUPS/source review found no recognized
ZTO candidates and unverified source at 26137142; typed agreement-gated balance
returned 0 with both ending block hashes matching. Live positive UUPS/source
candidate discovery remains untested; fixture coverage is explicit.
