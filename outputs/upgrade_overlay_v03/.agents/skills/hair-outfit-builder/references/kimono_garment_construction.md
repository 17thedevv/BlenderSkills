# Kimono-inspired Anime Garment — Constructive Modeling Reference

**Not a universal sewing pattern.** Kagari is a stylized kimono-inspired costume. Follow the actual concept rather than forcing historically exact construction. Inferred regions must be marked as inferred.

## 1. Identify garment masses BEFORE geometry

1. Inner cream layer under neckline: separate cloth surface with its own opening and chest silhouette.
2. Burgundy crossing collar/lapel: distinguish **collar vs draped front panel**. Verify which part crosses over which in Kagari's reference; record image evidence. Do not build a giant X-shaped decal hovering over the body.
3. Cream outer garment: its shoulder, sleeve volume and torso shape must exist independently of surface coloring.
4. Burgundy ornamental long strips/borders: decide whether trim stitched to cloth, fabric sash, or independent hanging strap. Each behaves differently in side view and animation.
5. Embroidery and star pendant are later detail passes.

## 2. Blockout procedure (Blender-agnostic modeling goals)

- Start from shoulders/neck/upper torso, anatomical/clothing clearance adequate for intended arm rig. Choose a neutral pose representative of rig rest pose.
- Establish approximate collar **cross-sectional depth**: inner edge near body, outer edge projected slightly outwards, seam contact, visible thin thickness at neckline. Do not hardcode millimeter thickness without scene scale; validate at bust and portrait crops.
- Build collar from broad, smoothly curved strips or surfaced patch geometry, not UV-only polygons or straight rods. Its **surface normals must transition** around neck, clavicle and chest. Symmetry may not match asymmetric overlap.
- Build sleeve as a **hollow, draping fabric volume** linked to shoulder seam; sleeve opening must remain readable in side/back. Separate sleeve outer surface / internal opening where necessary.
- Add **macro folds at plausible anchors**: shoulder seam, armpit, bent elbow, collar/chest contact, sleeve opening. No random uniform sinusoidal folds. Use broad low-frequency folds in silhouette first; smaller folds later.
- Keep cloth shell reasonable for weighting. Test arm raise and crossing arms before intricate surfaces. Collisions with body are expected to require per-pose fixes; do not let shrinkwrap flatten all drape.

## 3. Camera acceptance

- FRONT: collar overlaps clearly; no giant flat burgundy X detached from white body; overall silhouette matches reference.
- 3/4: visible depth and edge thickness; collars should not read as levitating strips; no intersection through chest.
- SIDE: true garment volume and sleeve opening; accessory not sunk into torso; neck region without hard creases not in concept.
- REAR: coherent shoulder-sleeve join and robe drape, rather than white sphere/solid shell or disconnected panels.
- POSE: at least neutral and moderate upper-arm raise; inspect shoulder deformation and collar collisions. Record exact arm rotation and render frame.

## 4. Bad/good diagnostic pairs

| Bad outcome | Likely cause | Corrective modeling action |
|---|---|---|
| Burgundy strips float above torso | Decoration modeled as free ribbon | Rebuild collar with seam/attachment and curved cross-section |
| Shoulder resembles a solid rounded sphere | Garment merely shrinkwrapped to torso | Add cloth volume, sleeve opening and seam transition |
| Cloth looks blank after gold details added | No macro folds or panel structure | Return to neutral clay and work on seams/folds |
| Sleeve crumples at shoulder pose | Missing deformation loops / weights | Rework sleeve shoulder mesh and weight test before texture |
| Gold piping inflates triangle count | Beveled curves with excess resolution | Use texture/UV for flat strokes, lower curve resolution for true edges |

## 5. Exit requirements

If no approved side/back reference exists, propose hidden construction alternatives and state the adopted interpretation. Require human approval for the structural garment clay pass **before** floral/trim decoration.
