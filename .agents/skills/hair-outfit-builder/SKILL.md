---
name: hair-outfit-builder
description: Produces coherent stylized VTuber hair clumps, outfit layers and accessories that keep appealing silhouettes and rig cleanly in Blender. Use after approved face blockout.
---
# Hair and Outfit Builder

## v0.3 construction gate

Read the active project state, design contract and actual references. Preserve the current face, morphs, rig, UVs, hair and unrelated assets; record a source backup and artifact SHA before edits. Distinguish observed structures from inferred side/back construction.

- For collar, robe and sleeve work, read [garment construction](references/kimono_garment_construction.md). Before geometry, document inner/outer layers, overlap order, seam contacts, shoulder/sleeve junctions, fold anchors and attachment weights.
- For hair work, read [hair form](references/anime_hair_form.md). Preserve roots, cap coverage, major clumps and taper; avoid an unbroken rectangular rear curtain.
- For ornaments or material work, read [materials versus geometry](references/materials_vs_geometry.md). Test one representative exported material/ornament before repeating it when export tooling is available.

Build large and medium garment forms in neutral clay first, with modest topology and no decorative shader, embroidery or gold piping. Collar bands must be attached to garment seams and wrap neck/chest; sleeves must be hollow volumes with readable openings. Use pattern surfaces, controlled modeling, shrinkwrap with clearance or cloth-supported construction according to the actual mesh; no base mesh or algorithm is mandatory.

Inspect matched front, 3/4, side, back and a moderate arm raise before ornamentation. A complete image set and valid mesh are evidence, not aesthetic approval. Stop for human clay-form approval before adding decoration. After at most three ineffective targeted cycles, recommend a different construction method or suitable licensed base garment.

Cloth around shoulders requires deformation weights across chest/shoulder/arm regions; a single chest-bone attachment is only a declared static preview. Measure raw/evaluated triangles and largest modifier expansion before repeating details. Store candidate/version/SHA and exact render/pose settings in the project state.

## Existing production checks

1. Plan hair hierarchy: skull cap, primary silhouette locks, secondary locks, a few accent strands. Distinguish bangs from side/back hair with depth.
2. Prefer purposeful tapered sections and controllable curve/mesh profiles; avoid forests of cylinders and floating spikes. Check scalp coverage and head movement clearance.
3. Outfit from major shape masses: neck/torso, sleeves, gloves/accessories. Prioritize streamer upper body; reduce hidden polygon/detail costs.
4. Separate rigid accessories from bend regions; choose bone-parenting for rigid parts and weighted mesh for cloth, with simplified secondary-motion rig later if desired.
5. Test camera angles and movements for collisions: bangs vs eyebrows/eyes, hair vs shoulders, sleeves vs wrists, cloth vs hips.
6. Use 3-color hierarchy unless brief specifies otherwise. Validate color/value separation with diffuse-only/neutral lighting preview.
7. Record all external textures and materials in license manifest.

**Exit:** readable front/3/4 hair+outfit silhouette, no major default-pose clipping, documented object naming and attachment plan.
