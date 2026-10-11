# Kagari concept-directed garment study — plan before modeling

User instruction: rebuild according to the concept. This authorizes a new construction approach; it does not approve the previous garment or unlock decoration/material work. Further Skills development remains paused.

Active reference: `outputs/design/concept_option2_kagari.jpg`, the only Kagari concept image currently in outputs/design. No new image was attached. Observed: broad curved crossed lapels, a narrow waist, sloping shoulder, long flared cream sleeves and restrained broad folds. The printed burgundy, gold trim, embroidery, pendant and hair are outside this clay study. Side/back construction is inferred.

Construct new meshes on the existing duplicate mannequin, discarding the failed panel/drape geometry from this new scene. Author in an arms-down pose (60 degrees below horizontal), close to the frontal concept rather than the earlier 30-degree study. Use manually controlled sheet panels and anatomical shoulder curves. Do not run Cloth: the outline, panel overlap and fold anchors will be explicit inputs, not simulation outcomes.

Layers: right under-front and left over-front; left collar leaf sits 5 mm ahead at the chest crossover, then extends diagonally toward the waist. A continuously sampled nape band joins both leaves. The broad collar edges contact their supporting panels. Neutral clay only, 1.5 mm support thickness and 1.8 mm collar thickness at meter scale.

Seams: two front patches join a back patch through a curved shoulder bridge. Positive-X sleeve front/back root edges share torso vertices; the sleeve top cross-section shares the shoulder edge. Side seams start below the open armhole. The one sleeve is two long sheets with rounded top/bottom connecting folds and a wide distal opening. Its silhouette extends along the forearm and flares below it; it is not a short radial tube.

Macro folds: shallow torso ridges taper toward waist and armhole; one soft sleeve valley is anchored below the armhole, another near the lower cuff. Back folds remain sparse. No high-frequency wrinkles or embellishments.

Skinning: chest/upperChest/shoulder transition at the root, upper/lower arm blend farther down the sleeve. Inverse blended skinning converts the authored arms-down geometry to rest coordinates. Moderate +30-degree raise and optional horizontal +60-degree stress test are ordinary Armature deformation only. No live Cloth or corrective morph hides the pose test. Frozen cloth volume is an acknowledged runtime limitation.

Save as a separate candidate. Render matched front, 3/4, side, back, moderate arm raise, plus horizontal stress. Rerender the previous study and Cycle 03 using the same mannequin, camera and pose where feasible. Inspect every candidate view. Report actual mesh counts and defects; stop for human review.
