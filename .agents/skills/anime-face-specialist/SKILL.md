---
name: anime-face-specialist
description: Refines anime-style VTuber head, facial proportions, eyes, eyelids, mouth topology and expressive readability. Use for face modeling, front/side silhouette correction and preparing blendshapes.
---
# Anime Face Specialist

**Do not attempt intricate face modeling before front and 3/4 view review.**

1. Freeze approved eye-level, jawline, cheek mass, head width/height and chin position from user reference. Create side and front guides.
2. Refine large forms before details: cranial mass and jaw => eye sockets and silhouette => upper/lower lids => eyebrows, nose, mouth => iris highlights.
3. Ensure closed eyes are a *real deformation*, not merely textures disappearing; preserve loops or engineered shape-key mesh to support blink. A separate eye/face material may be needed for anime styling.
4. Mouth must support 5 readable viseme silhouettes (AA, IH, OU, EE, OH) at streamer crop; don't generate them by indiscriminately uniform scaling.
5. Test eye direction, head yaw/pitch and expression extremes. Face symmetry is a baseline, not mandatory stylistic symmetry.
6. Make neutral expression appealing first. Do not rely on lighting to mask faulty geometry. Use `visual-critic` on actual front, 3/4, side, face-close render at fixed camera.

**Reject if:** flat featureless face, eye asymmetry not justified by concept, eyelashes floating, ugly jaw silhouette, mouth clips through cheeks or wink collapses.

**Exit:** reviewed head WIP with named expression shape keys and Gate B approval state. Shape keys alone do NOT configure VRM expressions.

## Webcam-centric priorities (v0.2)
- Judge whether the avatar's eyes and eyelid motion remain visually readable beneath its approved hair design. This concerns rendered expression readability and collisions; webcam recognition observes the human operator, not the avatar's bangs.
- Before adding eyebrows, lashes, eye reflections and mouth details, render 3/4 front portrait **at intended OBS crop**. Reinspect after outfit/hair changes.
- Engineer viseme and blink morphs for reliable midrange (0.5) as well as extremes (1.0); optimize visual clarity over mechanical exaggeration.
- Support VRM eye bones for gaze, with lid shape keys; keep ARKit Perfect Sync optional rather than pretending every anime face has 52 shapes.
