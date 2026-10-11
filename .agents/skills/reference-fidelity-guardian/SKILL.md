---
name: reference-fidelity-guardian
description: Protects approved character identity during 2D-to-3D work using observable landmarks, explicit inferred regions, scoped change checks and linked human review evidence.
---
# Reference Fidelity Guardian

Read the active project's design contract and actual concept files. Character-specific palette, hairstyle, accessories and reference paths belong in project config, not this generic skill. Preserve the user's identifying choices and current authorized scope.

## Reference and impact checks

1. Inventory source angles and distinguish visible forms from inferred rear/profile construction. Do not claim 1:1 physical correspondence from one illustrated view.
2. Record must-preserve markers and at least three useful landmarks for the edited region, such as collar crossing height, shoulder breadth relative to head, and sleeve width/depth. Estimate or mark NOT_OBSERVABLE when art perspective prevents measurement.
3. Present source and matched candidate view side by side. Classify elements MATCH, INTERPRETED, MISMATCH or NOT_OBSERVABLE with image evidence; use [the comparison template](references/fidelity_report_template.md).
4. Make a scope note before edits. Outfit-only work preserves face geometry/morphs, rig and hair; compare coordinates and bindings afterward. Invalidate only tests affected by the change.
5. Prefer a usable editable base with documented source/license and good construction. No particular mesh filename is mandatory; compare alternatives if the current topology prevents the requested form.
6. Judge garment/hair volume, seams, silhouette and motion rather than banning every scripted or surface-based method. Flat strips cannot substitute for the required cloth mass.

## Human review

Only linked explicit user visual approval unlocks an art gate. Code execution, a report written by the agent or a successful render do not constitute approval. Stop on an unauthorized identity change, propose the smallest correction, and record pending verdict separately from the agent's assessment.

Human webcam capture quality and avatar expression readability are separate. Avatar bangs affect visual readability and collisions; the tracker observes the human webcam feed.

**Exit:** version/SHA-linked reference delta report and exact images, with APPROVED_BY_USER only when backed by actual user evidence; otherwise REQUIRES_HUMAN_ART_REVIEW.
