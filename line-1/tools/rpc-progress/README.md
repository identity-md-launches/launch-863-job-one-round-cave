# RPC Progress

Watch whether a public Ethereum RPC head actually moves during a bounded window.
Python standard library only. Reuses the existing RPC Sampling and RPC Health
tools, so keep their sibling directories when copying this tool.

From the repository root, run the deterministic offline demonstration:

```sh
python3 -B line-1/tools/rpc-progress/progress.py --demo
```

For real mainnet reads against PublicNode and dRPC:

```sh
python3 -B line-1/tools/rpc-progress/progress.py
```

Defaults are three rounds, a 13-second pause after each round, a 12-second
per-request timeout and a 120-second freshness threshold. Repeat `--endpoint`
for public HTTPS URLs; never supply secrets. Credentials, queries and fragments
are rejected. Sampling bounds remain 1–8 distinct endpoints, 1–20 rounds,
0–60 second pauses, timeout 0.001–30 seconds, maximum age 0–3600 seconds.

JSON preserves every original observation and adds a per-provider `progress`
report: advancing transitions, identical adjacent heads, longest identical run,
backward heights and changed hashes at previously seen heights. Error gaps break
consecutive-run and adjacent-height comparisons; remembered hashes survive gaps.
Hash comparison ignores letter case. Stale observations still supply anomaly
evidence but cannot yield a healthy progress result.

Exit 0 means every provider had an observed advance with no errors, stale samples
or detected anomalies. Exit 1 requests review, including when no advance was
observed. Exit 2 is invalid input. Nothing is written by the tool: JSON goes to
stdout. It uses only `eth_chainId` and `eth_getBlockByNumber`, with an explicit
User-Agent, bounded response bodies, and disabled environment proxy discovery.

## Tried

The offline demo passed 13 checks on 2026-10-07: advancing/repeated heads,
single/empty windows, backward movement, changed hashes, stale data, error gaps,
case normalization and integration with the inherited sampler. The live run and
exact observed heights are recorded in `artifacts/line-1/progress-live.json` and
the round report.

## Limits

An unchanged head is an observation, not proof of a stalled provider: block
production intervals vary and caches can be normal. Regressions or changed hashes
can reflect real reorganizations or load-balancing, not necessarily dishonesty.
Only sampled heads are compared; intervening reorganizations can be missed.
Provider requests are sequential and pauses are not a fixed sampling frequency.
Local clock error affects freshness. This does not establish uptime, independent
providers, cross-provider agreement or future reliability. Use RPC Agreement for
the separate common-height check. No coin is needed for this public read tool.
