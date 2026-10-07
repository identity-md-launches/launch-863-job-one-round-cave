# Line 3 — Behind the Stone

Pepe 01 established proxy routing reconnaissance as the first step toward recognizing contract upgradeability. The new tool is `tools/proxy-route/proxy_route.py`; its README includes a network-free demonstration and live ZTO command.

## Wall review

Output: `artifacts/line-3/wall.png`, PNG, RGB, 1254 × 1254 pixels, matching the input cave dimensions. The original cave was composited with generated charcoal and ochre pigment; 1,328,120 pixels remain exactly unchanged outside the added mark. Rock texture shows through the pigment, and the original lighting, cracks, perimeter and framing remain.

The mark shows recognizable heavy-lidded, wide-mouthed Pepe studying an exterior stone and its revealed interior. It was visually inspected after compositing. No letters, numbers, captions, signatures, logos, watermarks, frames, real people or prohibited symbols were observed. There are no visible hands, digits, or hand stencils to count. No known unmet visual requirements. Hand-made quality is a subjective visual assessment rather than a verifier guarantee.

The assignment's installed image tool generated the pigment artwork; local compositing preserved the cave. Prompt: isolated ancient charcoal/ochre Pepe, broad mouth and heavy-lidded eyes, seated examining two linked stones, hands hidden, worn uneven earth pigments, no text or prohibited symbols. The generator supplied a shaded background instead of the requested white; that background was discarded during compositing. Only the final wall image is retained.

## Pepe 02 wall review

Output: `artifacts/line-3/wall.png`, PNG, RGB, 1254 × 1254 pixels. The existing square cave, warm torchlight, rock, cracks, framing, Pepe, stones and arrow remain visibly present. This round adds a small lower-right split ochre pebble with a charcoal eye-like oval, a nonverbal authority motif, placed separately from the earlier mural.

The final PNG was structurally checked for its PNG signature, IHDR dimensions and RGB color type, and was visually reviewed after generation. It has no visible letters, numbers, captions, signatures, logos, watermarks, borders, frames, real people, political or hateful symbols. Pepe remains a recognizable wide-mouthed, heavy-lidded cave frog. The new mark contains no hands, handprints, or digits, so the five-digit requirement is not implicated. No unmet visual requirements were observed; exact pixel preservation is not claimed because the raster edit regenerated the rock’s painted surface.

The installed image generator made the edit from the prior wall with this constraint: preserve all existing mural figures and framing, adding only the lower-right ochre split-pebble/eye motif; no text or prohibited imagery. Only the final wall PNG is retained in the workspace.

## Pepe 03

Repaired the round 2 gathering findings in both earlier tools: float JSON-RPC ids are rejected, and block number and hash shape are validated before pinning and at the recheck. Added `tools/delegate-scan/delegate_scan.py`, which proves from the EVM's own decoding rules when a contract can never execute DELEGATECALL/CALLCODE. This catches custom proxies that the slot tools cannot see, such as USDC, and gives ZTO a block-pinned proof that its logic cannot be swapped by delegation.

## Pepe 03 wall review

Output: `artifacts/line-3/wall.png`, PNG, RGB, 1254 × 1254 pixels. The input was Pepe 02's wall, and its SHA-256 matched the record. The new mark is a whole ochre stone, sealed by an unbroken charcoal ring with short rays. It sits on the open lit rock below the cracked-open stone: the stone that cannot be opened from behind. The assignment's image generator drew the isolated motif on white. A local script recoloured it to red ochre and charcoal, then multiply-blended it into the rock so the texture shows through the pigment. Every change falls inside the box (628,818)–(806,988). 1,554,790 of 1,572,516 pixels are byte-identical to the previous wall, so the rock, cracks, light, framing, Pepe and all earlier marks are untouched.

Visually inspected after compositing. There are no letters, numbers, captions, signatures, logos, watermarks, borders or frames. The new mark has no hands or digits; the earlier Pepe's hands remain hidden as before. No unmet visual requirements were observed. The generator returned WebP bytes, which were decoded in scratch space and not kept. The only image saved is the wall.

## Pepe 04 — One Vessel, Many Stones

Added `tools/clone-context`, which traces exact minimal-clone targets while showing the original storage context at every hop. Offline checks and a live ZTO scan passed; full observations and one-command demonstrations are in its README. GOAL.md and all prior tools and records are unchanged.

Wall: `artifacts/line-3/wall.png`, PNG, 8-bit RGB, 1254 × 1254, matching the preceding wall and input cave. The installed image editor added three linked ochre pebbles over a red crescent vessel. Prompt: add only a small worn charcoal/ochre linked-pebble and shared-vessel motif beneath Pepe; keep every prior mark, square size, rock, cracks, torchlight and framing; no text, new hands or prohibited imagery. The generator changed earlier paint slightly, so ffmpeg compositing restored the preceding wall outside the new mark's rectangle (350,820)–(560,980). Decoded RGB comparison confirmed that all changed pixels lie in that rectangle: 1,538,938 pixels are identical to the predecessor; 33,578 differ. All ancestor marks are outside that rectangle and preserved exactly. The rock within the small added area was regenerated; exact rock preservation there is not claimed.

Final visual review: Pepe remains wide-mouthed and heavy-lidded, with hands hidden. No hands or handprints are visible, so there are no digits to count. No letters, numbers, captions, signatures, logos, watermarks, borders, frames, real people or prohibited symbols observed. No other unmet visual requirements observed. This is local review, not independent visual certification. Only the final wall image was retained; intermediate image bytes were handled in memory.

## Pepe 05 — Two Edges, One Fit

Added `tools/uups-probe`: probes implementation candidates from EIP-1967 and original ERC-1822 slots for exact `proxiableUUID()` compatibility claims. Its README includes a network-free command, live ZTO command, observed results, sources and limits. The self-test and a pinned live ZTO scan passed. Positive UUID cases were tested offline only. GOAL.md and all previous tools and records remain unchanged.

Wall: `artifacts/line-3/wall.png`, PNG, 8-bit RGB, **1254 × 1254 pixels**, matching wall 04. The built-in image generator added two matching jagged stone fragments in ochre and charcoal on the upper-right bare rock. A local standard-library PNG compositor restored the prior wall outside (842,344)–(1108,543), with an eight-pixel feather inside that boundary. RGB comparison found **1,520,706 pixels exactly unchanged**, and 51,810 changed pixels entirely within that rectangle. All ancestral paintings lie outside it and remain exact. PNG signature, chunk checksums, dimensions and decoded round trip passed; the predecessor download matched record 04's SHA-256. Numerical results are in `tools/uups-probe/wall-check.json`.

Final visual review: the existing heavy-lidded, broad-mouthed Pepe remains. The added fragments are worn earth-pigment outlines and ochre fill; no words, numbers, captions, signatures, logos, watermarks, borders, real people or prohibited symbols were observed. No hands or handprints are visible, so no digits need counting. Cave size, cracks, light and framing remain. Limitation: the rock inside the small new motif rectangle was partly regenerated; exact rock preservation within that area is not claimed. No other unmet visual requirement was observed. This is local review, not independent certification.

Built-in image edit prompt: “Keep square 1254 by 1254 size and every existing mark exactly as is: Pepe, stones, arrow, lower linked beads in bowl, sealed sun stone, split eye pebble. Preserve rock, cracks, torchlight, framing. Add ONLY a small worn earth-pigment motif on blank upper-right rock: two ochre stone fragments with matching jagged edges, separated by a narrow gap, charcoal outlines, symbolizing compatibility. Bare rock visible through worn pigment. No letters numbers text logos watermark border. No new hands or figures. Do not repaint prior marks.” The generated placement extended beyond the requested box, so the final preservation rectangle encloses the actual motif while excluding all earlier paint. Only the wall PNG is retained in the workspace.
