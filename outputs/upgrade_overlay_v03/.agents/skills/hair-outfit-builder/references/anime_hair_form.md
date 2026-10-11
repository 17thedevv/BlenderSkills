# Anime Hair Volume Reference — Kagari case study

## Distinguish form from graphics
- Hair has a **scalp cap**, masses emerging from roots, major sweep lines, secondary splits, and thin strands only at edges. Highlights are a shader/texture issue, not an excuse to create flat panels.
- Maintain distinct depth among front bangs, side framing locks, back mass and offset ponytail. In 3⁄4, the silhouette should have natural volume, not stacks of flat layers.
- For Kagari: honey-brown hair, soft rounded bob/fringe frame, long side ponytail with burgundy ribbon and small gold floral details. Determine precise side from authoritative concept image orientation. Avoid accidentally mirroring the whole hairstyle.
- Confirm bangs' shape from concept; if hidden areas are unknown, interpret minimally and record uncertainty.

## Modeling progression
1. Isolate hair to neutral materials; render front/3⁄4/side/back silhouette.
2. Replace exposed black/purple scalp gaps and hair chunks cutting into ears.
3. Create primary locks: roots attached to scalp, volume through middle, believable taper and curved tips. Flat straight-cut rear curtain → split into controlled tapered masses with staggered ends.
4. Establish ponytail anchor on proper side, flowing from roots to tie point with realistic bundling; check connection to scalp/back mass.
5. Ribbon: bow loops with depth and tails that hang under gravity; avoid perfectly flat triangles and floating rigid planes. Parent/weight to an anchor, optionally use simple spring bones after rig is stable.
6. Only then add strand grooves and warm highlight modulation without saturated yellow glowing bands.

## Validation
- Front: face frame and brow/eye readability; no forced requirement that eyebrows remain fully exposed for camera tracking (camera sees the HUMAN, not this avatar).
- Side: hair volume and head profile; no disconnected root.
- Back: no flat rectangular slab, exposed cap or blunt straight chopped baseline unless concept explicitly calls for it.
- Motion: head turn ±30°, nod/pitch and moderate shoulder swing; inspect intersections and bow/ponytail behavior.
- Export: confirm chosen hair shader and alpha settings survive a representative VRM export/re-import before decorating whole hair.
