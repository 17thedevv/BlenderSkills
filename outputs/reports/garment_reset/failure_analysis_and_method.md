# Kagari garment construction strategy reset

## Inspected evidence

Loaded the real `outputs/wip/kagari_v03_clay_03.blend` in Blender 4.2.0. Artifact SHA256: `4a3dc7560df7d3f0db452a4d0c06faf55238bce2fd045ed23f8c27ac75dd6051`.
Inspected all eight actual PNGs in `outputs/previews/v03_clay_cycle03`: front, three_quarter, side, back, pose_arm_raise, portrait, side_garment_isolated and back_garment_isolated. The isolated diagnostic views are essential because Hair obscures the rear shoulder. Object/topology/bone/addon evidence is in `artifact_and_tools.json`; construction code is in `scripts/build_kagari_v03_clay_pattern.py` and `scripts/build_kagari_v03_clay_cycle03.py`.

| Failure | Responsible geometry/method | Actual render evidence | Structural cause versus detail |
|---|---|---|---|
| Rigid cylindrical/bell sleeves | `Kagari_v03_Outer_Robe_And_Sleeves`: nine generated rings around the upper-arm axis, normalized radial directions, nearly fixed radius .061–.074 m | front, three_quarter, isolated side; raised pose | Ring construction models a tube with radial clearance. It has no hanging front/back fabric bag, planar cut, seam tension or gravity equilibrium. Small folds would only decorate this tube. |
| Unnatural shoulder/sleeve | Same object; an arbitrary rectangular hole in the torso ring grid is bridged to sleeve rings. Cycle 03 narrows the torso top by .071 m without rebuilding the sleeve armhole geometry | isolated side/back expose skin and hard segmented ridges; front shows cut-looking joins | Geometric shoulder/yoke and armhole do not correspond to the anatomy or a cloth pattern. The top contraction changes the silhouette while preserving a bad junction. More polygons cannot fix it. |
| Incorrect collar overlap | `Kagari_v03_Sewn_Cross_Collar` follows a V-top ring and radial band offsets; `Kagari_v03_Attached_Over_Wrap_Edge` is separately solved onto the torso envelope | front and portrait pinched crossing, three_quarter distorted throat | A V-shaped neck ring plus a projected strip is not two overlapping front garment panels. Neck contact, hidden edge and true layer order were not constructed together. |
| Flat torso/back | Outer and inner surfaces use elliptical sections and height interpolation, with a small procedural front ridge | isolated back is smooth cylinder; front slab-like envelope | No fabric rest dimensions, hem slack, seam anchors or drape. The front Gaussian ridge is not an equilibrium fold. Lack of construction mass, not missing ornament. |
| Rigid sash | Existing `Kagari_Obi_Woven_Band` with broad elliptical bounds x ±.18, y -.158..+.182, z .907.. .974 | front/side show a wide extruded belt block | Independent regular belt geometry has no compression/conformity/tie tension. It was preserved, not newly improved. Out of the limited reset prototype: omit it instead of adding detail. |
| Poor raised-arm deformation | Sleeve generated in the posed space and inverted through LBS; hand-assigned arm weight ramps and chest-dominant torso; no collision/rest-length solver during the pose | arm_raise exposes creases/ridges at root | Binding keeps vertices moving, but cannot preserve fabric volume, avoid body collisions or correct the armhole. Normalized weights do not prove deformation quality. |

The first five issues require changing construction, boundaries and material distribution. Additional subdivision, embroidered piping, thickness or noise cannot supply a missing cloth panel or correct seam order.

## Available tools and selected method

Inspection confirms the locally installed Blender 4.2.0 binary, native Cloth/Collision types, Edit Mesh tools, Armature, skin groups and registered VRM operators. Registered addon inventory includes Rigify and the existing VRM addon; no garment-specialist addon was found among registered modules. `D:/tools` contains Blender and VRM setup scripts. No Marvelous Designer/CLO/Browzwear-named folder was identified at the inspected Program Files root. These are scoped inspections, not proof that no other software exists anywhere. No installation or external asset download was performed.

| Option | Merit for this small study | Cost/risk | Selection |
|---|---|---|---|
| Pure Blender-native free cloth/sewing | Genuine gravity, contact and seam forces | Flat panels must be placed correctly; sewing can pull through the mannequin; solver/cache is not directly portable to VRM | Use native Cloth for draping, not an unconstrained full sewing solve |
| Pattern modeling only | Explicit front/back cuts and connected seams; easiest topology/rig control | Authored folds alone can remain stiff; no gravity/contact evidence | Use for the initial panel surfaces and seams |
| Pattern panels + welded seams + native Cloth drape + frozen mesh | Supplies pattern mass and gravity folds while keeping known vertex correspondence and conventional weights | Static freeze must be tested under poses; live gravity behavior is not preserved by ordinary skinning | **Selected: smallest installed workflow with a plausible rig/export path** |
| Dedicated garment application/addon | Pattern iteration and sewing UI could be easier for a complete outfit | Not verified available in inspected inventory; install/license/integration overhead | Not needed or installed in this task |

The Blender manual documents [freezing a Cloth result and pinning clothing to an armature](https://docs.blender.org/manual/en/4.4/physics/cloth/examples.html). The local 4.2 API and an actual solver execution establish availability for this project. Pin the structural anchors, add Collision to the mannequin, let the free fabric settle, and retain a static result with standard Armature deformation. Motion cloth remains a separate Blender feature, not a VRM guarantee.

The initial seam connection is made explicitly with shared mesh indices and bridge faces, avoiding the instability of a separate sewing-spring join. The sleeve is two broad sheet grids with a lower seam and distal opening. It is fundamentally different from a normalized radial ring sweep. A collar band finishes the boundaries of two genuinely overlapping front panels; its order comes from those panels, not from a free X strip.

## Pose interpretation

The duplicate mannequin uses arms 30 degrees down from horizontal for construction; only its left arm is raised by an additional 30 degrees for the basic test. This makes the one-sleeve panel cut inspectable. The original eight Kagari renders are retained as failure evidence; a matched mannequin comparison will use this same study pose and framing for Cycle 03. This is not a full-character approval or a claim that a frozen sleeve supports every pose.
