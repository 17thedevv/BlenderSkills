# Garment Geometry Recovery — bounded repair plan

Source: full-kagari-concept-outfit-v3, SHA256
`ffbc443b2f4c1af194a77cbfdd1d4a4deb80e7b6ca1d0b1929a2dc767577fd16`.
Independent byte-identical backup verified before mesh edits. Maximum TWO repair iterations.

## Diagnosis and editable surfaces

- `Kagari_Concept_Robe_Two_Sleeves`: rays at x=.13,z=.975 hit sleeve faces
  3238/3688, not torso panels. Inner sleeve walls intersect the sash at its side/front/back.
  The old report described visible cream cloth crossing the sash; this inspection identifies
  that cloth more precisely. Move the low inner sleeve seam outward with a smooth vertical
  falloff while preserving its shared shoulder root and full sleeve opening.
- `Kagari_Concept_Soft_Waist_Sash`: its lower radius .150 is smaller than the lower robe at
  belt-bottom height; top overlaps the upper torso by only 2mm. Fit a slightly broader lower
  cross-section and higher upper edge around the inner garments, with a clear layer gap.
  This is geometry/layer repair, not a material or framing change.
- `Kagari_Concept_Crossed_Collar`: nape outer edge reaches y=.081 while support is around
  y=.067 at the back neck. Reduce radial shelf width and lower the inner arc; attach the
  outer arc near the actual rear neckline. Keep front overlap and leaf endpoint indices.
- Shoulder bridges of the robe retain matching quad sampling and shared sleeve root vertices.
  Relax their excess crown height and add only a few broad folds anchored at shoulder/seam
  positions. Preserve clearance to skin and use unchanged armature weights initially.

Layer order: Body display/inner top → cream torso/lower robe → burgundy sash;
burgundy collar above its cream support. Sleeves remain separate in space from sash,
but remain topologically joined to torso at their original roots.

No new vertices/faces, subdivision, materials or ornaments in iteration 1. No face/hair,
lower robe, rig/rest pose, animation or export edits. Existing inferred back/lower design
is not a newly approved reference. Front collar order remains the v3 over/under arrangement.

## Evidence and stop rule

Reuse full-v3 clay/color camera and lighting settings. Inspect front/3q clay+color,
side/back clay, saved neutral and existing raised/horizontal arm poses. Count raw/evaluated
triangles and modifier contribution; verify positive normalized weights and original protected
data after reload. Report actual image findings and bounded intersection diagnostics separately
from any all-pose claim. If a second repair remains unreliable, stop and explain the method limit.
Full art gate remains pending human approval; exposed scalp is inherited and outside this task.
