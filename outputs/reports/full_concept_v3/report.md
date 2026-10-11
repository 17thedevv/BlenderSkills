# Kagari — complete avatar with revised garment construction

**Construction delivered as a complete .blend WIP. Artistic gate: FAIL / requires human review.**

The full avatar now wears the revised crossed collar, connected torso and two long wide sleeves,
a softer narrow sash and a new waist-to-ankle robe. Face, hair, original Body data, all Face morph
coordinates/values, UVs, weights, rig rest data and saved pose match the original after reload.
This is a full-avatar integration of the corrected study, not a face/hair rebuild or final VRM.

- Candidate: [kagari_full_concept_v3.blend](../../wip/kagari_full_concept_v3.blend)
- Version: `full-kagari-concept-outfit-v3`
- SHA256: `ffbc443b2f4c1af194a77cbfdd1d4a4deb80e7b6ca1d0b1929a2dc767577fd16`
- Review: [interactive comparison](../../previews/full_concept_v3/review.html)
- Source concept: [concept_option2_kagari.jpg](../../design/concept_option2_kagari.jpg)
- User scope: [full-model authorization](user_authorization.md)

## Construction method

Controlled cloth surfaces with explicit connected sleeve roots, inverse skinning into the existing
rig rest space, sparse large fold shapes and thin Solidify thickness. Both sleeve roots reuse the
torso vertices; the second sleeve mirrors only the sleeve, not a duplicate torso. The crossed
collar has ordered under/over leaves and a connected nape. This method preserves ordinary armature
deformation. It is not a sewn 2D-pattern physics simulation: drape and folds are authored, not
recomputed by a Cloth solver. The failed Cloth experiment and original Cycle03 stay untouched.

Existing cream and burgundy materials are reused for a color preview; neutral Workbench clay
is the primary construction evidence. No new embroidery, accessory, material design or software
installation. Working panel UVs exist but are not a final garment texture atlas.

The original Body includes obsolete clothing in the same mesh. It remains intact in
`ARCHIVE_Rejected_Garments_Do_Not_Export`. An independent `Body_GarmentDisplay` copy removes those
old cloth faces while retaining skin, shoes and inner upper torso. Body has no shape keys. The
new lower robe was required after the old skirt edge appeared as a sawtooth beneath the smaller
sash. Its long A-line silhouette is an inference; the reference supplies no lower/side/back views.
The archive remains in the file for recovery, not for eventual export.

## Visible comparison with Cycle03

| Region | Cycle03 | Integrated candidate |
|---|---|---|
| Sleeves | Short rigid cylindrical blocks | Long hollow flared cloth surfaces, readable cuff thickness |
| Shoulder | Detached-looking open joins | Shared root topology and continuous form on both sides |
| Collar | Pinched chest triangles and irregular crossing | Wider curved leaves with a much clearer crossing |
| Torso | Broad flat shell | Some waist/chest volume and folds; back remains too smooth |
| Waist | Large rigid cuboid band | Thinner curved band, but visible torso/sash overlap remains |
| Lower robe | Old cut cloth silhouette | Continuous new shell with a few vertical fold channels; still too smooth |
| Arm tests | Rigid raised short sleeve blocks | Continuous sleeves at raised and horizontal arms; broad frozen underarm bags |
| Hair | Scalp gaps and planar rear strips | Identical source geometry; these defects remain |

All nine clay comparisons use matching camera positions, scale, gray display and upper-arm pose.
Two arm tests are both arms raised 30 degrees from the saved pose (about 38 degrees below
horizontal), and upper arms horizontal. They are rendered armature poses, not animated cloth
or collision tests. Original saved pose is restored before preservation verification.

## Remaining defects and artistic decision

The candidate does not meet the no-visible-intersections criterion. Cream cloth cuts into the
burgundy sash near both front corners; rear waist joins have angular breaks. The nape collar is
still shelf-like, rest sleeves and lower skirt lack motivated folds, and the raised sleeve volume
looks like broad rounded bags. Side/back hair still exposes the old scalp and flat strips; the
scalp defect is a hard rejection under the visual rubric. The color preview makes the waist and
scalp defects especially clear. No artistic success or final concept fidelity is claimed.

Separate long haori lapels and the complete layer hierarchy remain incomplete; existing sneakers
also remain. Decorations were deliberately outside this construction request. Human review is
needed for the inferred full lower silhouette. This delivery stops after three integration
configurations with these defects disclosed, without declaring the avatar approved.

See [visual review](visual_review.json) for precise image evidence and next actions.

## Geometry and verification

| Scope | Raw triangles | Viewport evaluated triangles |
|---|---:|---:|
| Four new garment surfaces | 20,105 | 41,908 |
| Cycle03 five separate garment meshes | 6,880 | 17,544 |
| Candidate render-enabled inventory | 47,434 | 118,773 |
| Cycle03 render-enabled inventory | 36,741 | 96,941 |
| Candidate entire scene including hidden/archive | 86,936 | 189,019 |

The five old meshes exclude clothing embedded in Body; the four new surfaces include the lower
robe. These counts are not a like-for-like garment-only cost comparison. Render-enabled counts
use object hide_render and viewport modifiers, without simulating collection exclusion. They
are not final render/export counts, VRM triangle budgets or FPS measurements.

Each new garment surface is one connected component, with no zero-area faces or interior
nonmanifold edges. Open sheet boundaries are intentional and thickened by Solidify. All garment
vertices have normalized deform weights and no more than four influences. All armature modifiers
reference the original `Armature`. Evaluated positions are finite in saved, raised and horizontal
poses. Protected source data matches after reload. These technical checks do not prove art quality
or intersection freedom. [Technical verification](technical_verification.json),
[geometry audit](geometry_audit.json), [complexity details](mesh_complexity_comparison.json).

## VRM and rigging risks

- Hidden archived Body/old garments must be explicitly excluded from export to avoid duplicated skin/clothes.
- Skinning gives a fixed drape; no gravity response, skirt physics or full animation acceptance exists.
- New lower robe currently binds to hips/spine. Walking, leg raises and sitting are not tested;
  coat/skirt secondary bones need separate work before runtime use.
- Working UVs and inherited Blender shaders require eventual VRM/MToon validation; reused materials
  are not certified by successful Eevee rendering.
- Solidify cost, normals, export triangulation, VRM reimport, expressions and Warudo tracking remain untested.

No Skills expansion, ornamentation, material production or VRM export was performed. The full
construction requested by the user is delivered; the artistic acceptance gate remains unapproved.
