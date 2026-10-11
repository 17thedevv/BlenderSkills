# Controlled sewing-panel experiment — plan before geometry

Source: Recovery v2, used only for a copied upper-body mannequin/rig and a separately rendered comparison. No garment vertices are imported into the prototype generator. Original files and state have independent backups.

Chosen route: fresh, metric 2D panel grids placed around a T-pose mannequin; distinct seam vertices linked by loose-edge Blender Cloth sewing springs. No pinned shoulder bridge. Collar finishing band is generated from the sewn neckline after draping, with metric strip UVs and declared layer order. This is a hybrid sewing/drape workflow, not a specialist pattern CAD system.

Pieces: two overlapping front support cuts, one back support cut with neck opening, two rectangular sleeve panels (one sleeve only). Support ends at the upper torso; no sash/lower garment. Front left/positive-X leaf lies outside negative-X leaf. Sleeve has upper/bottom seams, partial distal seam and an open cuff; root joins shoulder/torso only above the underarm opening. Neck anchors only; shoulder and sleeve remain free. Side/back cuts are inferred from the front Kagari concept.

Run sewing in T-pose, move the duplicated arms gradually into Recovery v2's saved neutral pose, settle, then raise the sleeved arm by 30 degrees and to horizontal. Store actual simulated vertex snapshots, seam gaps, solver timing and movement evidence. Render frozen snapshots in fixed Recovery v2 clay cameras. Separately freeze the neutral result, assign conventional weights and render rig-only stress tests. These diagnostics must not be confused with simulated deformation or VRM behavior.

Thickness is a post-drape Solidify modifier, neutral clay only. Pattern/UV data, seam endpoints and sewing setup stay in a separate reproducible source scene. Weld only documented seam pairs in the frozen output; this operation does not improve the cloth shape. No subdivision during solving. Maximum three independent pattern/solver configurations; stop and report failures honestly. No full reconstruction, external downloads/installations, ornaments or production export.
