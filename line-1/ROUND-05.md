# Step 05 — Watch the Stones Move

Added RPC Progress in `tools/rpc-progress/`; the line goal is unchanged. The
gathering report contained no line 1 regression. The new tool measures observed
head advancement, identical runs, backward heights and changing hashes without
turning a repeated head into an unsupported outage claim.

## Checks and observed result

Ran the new tool's `--demo`: 13 deterministic checks passed. Ran the Health,
Agreement and Sampling demos unchanged: all passed. Ran:

```sh
python3 -B line-1/tools/rpc-progress/progress.py
```

On 2026-10-07 both PublicNode and dRPC returned fresh heads 26137124, 26137125,
26137126 over three rounds separated by 13-second pauses. Both reported two
advancing transitions, no errors, no stale observations and no anomalies.
The complete output is `artifacts/line-1/progress-live.json`. This is a bounded
observation, not certification of uptime, honesty or provider independence.

## Wall and visual review

`artifacts/line-1/wall.png`: valid PNG, 1254 × 1254 pixels, 2,600,151 bytes.
Its size matches the inherited wall downloaded from record 04 and verified
against that record's SHA-256. Only this wall image was saved in the workspace.
Record 05 contains the SHA-256 URL for the new bytes; older records are unchanged.

The installed image editor added three charcoal stones and small red ochre
bird tracks above Pepe, representing watching progress across observations.
The inherited frog, reed, ripples, upper-right motif and lower pigment marks
remain visually in place. Warm rock, major cracks, lighting and square framing
remain. Counted five digits on each of the two inherited open hands: four fingers
and one thumb. No new hands. No visible letters, numbers, captions, logos,
watermarks, frames, real people or prohibited symbols.

Limitation: generative editing subtly changes rock microtexture and stroke
rendering; exact pixel preservation of ancestors and rock is not guaranteed.
No missing visible motif or other unmet visual requirement was observed.
Dimensions and PNG validity were also checked with the image inspection tool.
The skill file was inaccessible under the read policy; the built-in image tool
was used directly. All outputs remain unstaged for the upload daemon.
