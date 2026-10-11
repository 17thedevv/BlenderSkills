# Ornament and Surface Detail: Material vs Geometry Decision

| Detail type | Preferred initial representation | Rationale |
|---|---|---|
| Flat gold embroidery/floral motifs | UV texture or atlas/MToon-compatible material | Not silhouette-changing; cheap compared with hundreds of curve bevel objects |
| Fabric color blocks | Material regions or UV texture | Color should not require physically separate floating panels |
| Collar hem/edge thickness | Actual manifold/open-surface geometry as needed | Changes 3/4 silhouette and close-up highlights |
| Pendant/star jewelry | Small dedicated geometry | Has real silhouette and swing/attachment |
| Gold piping in near-camera silhouette | Low-segment curve or very slim mesh when needed | Profile matters; cap curve resolution carefully |
| Tiny repeated seam stitches | Texture/normal detail when runtime supports | 3D stitches often waste geometry |
| Hair highlights | Toon shader/texture | Do not encode highlights with huge flat gold meshes |

**Rule of thumb:** If a detail is invisible in a grey clay render at the final OBS crop, do not spend geometry on it until structural appearance is approved. This is a decision heuristic, not an absolute prohibition.

Before mass duplication: prototype ONE repeatable ornament; record evaluated triangle count, materials, UV, size in OBS frame, and VRM render compatibility. Then decide whether duplication is worth it.
