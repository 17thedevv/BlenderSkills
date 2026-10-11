# VTuber visual quality rubric (human-confirmed)

Rubric uses five criteria scored 0 to 5. These are **subjective assessments** requiring actual inspection of Blender preview images. Automated scene audit is only a technical supplement. Do not fabricate numerical grades.

| Criterion | Weight | 5/5 benchmark |
|---|---:|---|
| Face appeal/readability | 30% | Consistent anime face, eye/lid symmetry, expressive neutral close-up, distinct character identity |
| Reference/style fidelity | 25% | Style, palette, silhouette match user's approved reference; recognizable at thumbnail size |
| Hair/outfit silhouettes | 15% | Clean shape language, coherent layers, no distracting shape collisions |
| Rig/deformation integrity | 15% | Neutral + extreme key poses stable, no visible intersections, basic facial motion believable |
| Expressions/motion | 15% | Blink, visemes and idle reads clearly at streaming crop and loops cleanly |

**Stage-specific gating:** during S1/S2 evaluate face/style first and mark rig/motion NOT APPLICABLE, rather than treating them as zero. Do not compute final weighted score until all criteria are assessable.

Repair pass:
1. Capture real preview with `scripts/render_review.py` and any targeted pose/expr shots.
2. List top 3 defects, each tied to a named region and concrete mesh/material/rig change.
3. Fix only prioritized issues; retain snapshots for before/after comparison.
4. Rerender exact same views and compare.
5. Maximum three aesthetic correction passes per gate; if unsolved ask user to guide style or use a better base mesh.

**Disqualifiers** even when numeric average is high: no user face approval; unsupported asset license; missing mouth/blink expression when required; obvious face clipping at idle; failed VRM re-import; fake screenshot evidence; claims of tested live tracking with no runtime access.

**Tracking reliability test:** preview expressions over a range of intensities (0%, 50%, 100%), combinations like smile+blink and mouth+blink, slight head pitch/yaw. A VRM add-on mapping is required; raw Blender shape key names do not automatically become standardized VRM expressions.

## Webcam-ready delivery addendum
- Expression combinations and tracking response must look coherent **at actual stream crop size**, in addition to studio renders.
- Runtime gate requires manual Warudo tracking checklist T01–T08. FPS and OBS gate requires T09–T11; a rigged `.blend` and a passing VRM parser do not imply success.
- Do not certify an unobserved webcam, OBS video, microphone, streaming connection, or actual GPU performance as PASS.
