# Streaming Performance and Fallback Strategy

Starting budget, not a benchmark or a runtime requirement:
- Aim for **30 FPS tracking + avatar + OBS** initially, measured on actual hardware and expected game load; do not claim achievement until measured.
- Start with about **80k triangles or fewer**, **2048px maximal initial texture edge**, and approximately **8 material slots or fewer** where sensible. These are adjustable heuristics, never absolute artistic limits.
- Begin with **head/shoulder crop** and one directional/key light; test portrait camera and broadcast framing. For lower powered hardware, simplify scene render/shadows/extra cameras before damaging approved face geometry.
- Treat hair chains and collider counts as budget items. Avoid adding live cloth simulation as the first milestone.

## Measurement protocol
Measure in four conditions: (A) Warudo with model static, (B) Warudo+MediaPipe, (C) +OBS capture, (D) +intended game under normal workload. Log FPS/latency if tools expose it, VRAM/CPU/GPU usage and obvious frame stutter. Compare same camera/framing for every run.

## Fallback
If GPU pressure: try lowering Warudo render resolution and expensive post effects, then switch MediaPipe from GPU to CPU **if CPU headroom exists**, or lower OBS/game GPU load. If tracking noisy, improve webcam light/calibration before costly additional face morphs. Keep `config/character_brief.json` and approved aesthetic gates in force after optimization.

Warudo guidance: https://docs.warudo.app/docs/mocap/mediapipe
