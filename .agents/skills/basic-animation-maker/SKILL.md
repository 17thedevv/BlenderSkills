---
name: basic-animation-maker
description: Builds and reviews simple loopable Blender VTuber animations such as idle breathing, blink, nod and wave, while preserving rig and facial expression correctness.
---
# Basic Animation Maker

1. Start from approved neutral pose and existing humanoid rig. Target separate named Actions: `idle_loop`, `nod`, `wave`. Natural blink can be driven by expression/target app, not necessarily baked inside idle Action.
2. Default timing at 30fps: idle 4-6s seamless loop; nod 1-2s; wave 2-3s. Adjust as character personality requires.
3. Animate torso/neck with restrained amplitudes; do not use unrealistic breast/head oscillation. Stagger shoulder, elbow and wrist motion subtly for organic wave.
4. Inspect start/end loop transforms and F-curve continuity; align phase and slope at boundaries (or use cyclic F-curve modifiers).
5. Inspect key frames, intermediate frames and expression overlap with animation. Produce motion preview or a sheet of several frame renders, not simply still image of frame 1.
6. Preserve authored Actions separately from VRM avatar export and design target-app compatible delivery strategy (e.g. VRMA if properly supported, animation files or runtime action playback). Do not assert `.vrm` automatically contains arbitrary animation Actions.
7. Report total frames, fps, rig version, dependencies and unresolved animation defects.

**Exit:** actions in `.blend`, optional exported animation asset, sampled frame preview, Gate E state.
