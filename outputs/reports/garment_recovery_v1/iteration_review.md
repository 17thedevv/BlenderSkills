# Iteration 1 — reviewed before second controlled repair

Candidate SHA256 `61df33536b9b8caebe9d2bccaa2d7599bb917f10476bb6c67fcc0dab318f61e4`.
9 actual clay and 4 existing-color renders visually inspected. Front/3q waist triangles disappear,
back sash becomes continuous and the nape shelf is reduced. Full v3 Face/Hair/Body/rig and all
untouched meshes match after reload. Triangle counts do not increase.

Bounded evaluated edge-to-triangle probes identify:
- Sleeve/robe–sash: 239→0 crossing segments in saved pose; 0 in raised/horizontal poses.
- Lower robe–sash: 592→0 in all three poses.
- Collar–robe at neck: 329→149 in saved/raised pose; remaining crossings at leaf/nape junction.
- Collar–Body at neck: 30→0 in saved pose.
- Robe–Body: 58 crossings in saved pose, 0 in raised pose, 450 in horizontal pose (source 244).

These are crossing-segment counts in declared height ranges, not intersection area, severity or
an all-pose certificate. The added sleeve clearance changes deformation near the forearm and
creates additional horizontal-pose contacts. Shoulder bulges and broad underarm bags remain.
Recommendation: FAIL to accept whole recovery as reliable at iteration 1. Use the ONE remaining
iteration to enforce local clearance to the body across the three existing poses and to separate
collar/support surfaces. No new topology, materials, hair/face changes or full-body animation.
