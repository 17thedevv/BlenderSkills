# Codex / Antigravity Task — Merge Kagari Artistic Skills Upgrade v0.3

You are the lead AI Technical Artist and Blender Pipeline Engineer for Kagari, a Japanese-anime female VRM 1.0 VTuber.

## Situation

The current model has clearly improved in reference identity but still shows severe garment form defects: burgundy strips read as decals, shoulders/sleeves are flat, hair rear sections are slab-like, and evaluated geometry expanded dramatically without proportional artistic improvement. The existing 13-Skill Kagari workspace has its own project-specific additions, while the provided upgrade is an **overlay derived from an earlier 12-Skill pack**. Therefore do not wholesale overwrite or regress the local workspace.

## Task A — Merge and verify existing state, before modeling

1. Locate local 13-Skill workspace, Git state, current `.blend`, concept image(s), audit report, signed-off face/head renders, current delivery files and Warudo/VRM tool status. Identify actual file paths; NEVER invent them.
2. Back up/commit working files before modifying. Diff these v0.3 overlay documents against current Skills; incorporate novel guidance while retaining valuable local content.
3. Keep generic modeling guidance in Skills and Kagari-specific fidelity details in project config. Do not hard-code the base mesh named `AvatarSample_B`; compare usable alternatives if needed, preserving provenance/license.
4. Add references under `hair-outfit-builder/references` and `visual-critic/references`, preserving YAML Skill frontmatter and any Antigravity discovery requirements. Update README to reflect actual skill count, not a hard-coded false claim.
5. Integrate new `scripts/audit_blend.py` carefully if existing audit has additional valuable checks. Preserve raw topology checks, evaluated depsgraph counts, shape keys, weighting warnings, and export distinction. If something cannot be counted, emit `NOT_TESTED` or error, never zero success.
6. Integrate `scripts/validate_project_state.py` independently of structural `check_skillpack.py`. Populate a real `config/project_state.json` from existing evidence, without fabricating approvals. Reconcile broken `outputs/DELIVERY.md` references. The state and DELIVERY must refer to the SAME current artifact and version.
7. Run structural and state validators, Python syntax/test checks, and Blender audit on real current candidate. Do not mark live VRM/Warudo tests as passed unless genuinely executed.

## Task B — ONE construction-quality experiment (clay only)

1. Identify Kagari's actual reference image and candidate `.blend` and take same-camera baseline renders.
2. Focus on **upper torso crossed burgundy collar and shoulder / top sleeve junction**. Preserve face, facial morphs, rig and hair without modification. Save to NEW WIP candidate; never destructively overwrite original.
3. Make a garment construction plan before writing geometry: inner cream top, overlap ordering and cloth contacts, burgundy collar/lapel strips as *real attached garment shapes*, cream outer layer and sleeve transition, actual seam and fold anchors.
4. Build only large and medium forms with neutral clay material. No floral patterns, gold trim, extra jewelry, decorative shader or texture changes. No dense modifier subdivisions until baseline form is approved.
5. Render front, 3/4, side, back and moderate arm raise with comparable lighting/cameras, and inspect the real images using image-capable tools. If visual inspection is unavailable, STOP and ask for user review.
6. Generate artifact SHA, exact evidence references, raw/evaluated triangle counts and largest modifier expansion list. Contrast form, silhouette and intersection flaws with baseline.
7. Produce top-three defect report with proposed geometry corrections. After at most 3 targeted ineffective cycles, stop and recommend another construction method or base garment.
8. STOP FOR USER APPROVAL. Do not proceed to gold trim, flowers, hair reconstruction, extensive rigging or final VRM export in this iteration.

## Acceptance criteria

- No misleading floating X-shaped collar ribbons: layers curve around chest and neck with plausible seam/edge thickness.
- Shoulder/sleeve join readable in profile and 3/4, moderate arm raise reasonably deforms without catastrophic clipping.
- Rendered shapes have meaningful cloth mass/folds in gray clay, independent of color/ornament.
- Current candidate, reports, renders, concept and approval status traceable to real paths and SHA.
- Geometry audit distinguishes Blender raw/evaluated and explicitly marks exported VRM and Warudo runtime untested unless verified.
- Human approves form before ornamentation.

## Deliverables

1. Small Skills/code diff with rationale.
2. Exact current candidate path/hash, baseline path/hash, source concept path.
3. Front/3/4/side/back/pose clay renders before and after, consistently framed.
4. Raw vs evaluated geometry report; modifier costs and top objects.
5. Visual defect and constructibility report.
6. Updated project_state.json and reconciled delivery manifest.
7. Decision: `REQUIRES_HUMAN_ART_REVIEW` unless the user has explicitly approved.

## No-go rules

- No repeated embroidery piping to hide flat collar.
- No fake progress updates or nonexistent artifact paths.
- No mass changes to face rig or hair on an outfit-only task.
- No claim that successful Blender rendering or valid geometry equals VTuber production readiness.
- No external asset download or payment without explicit permission.
