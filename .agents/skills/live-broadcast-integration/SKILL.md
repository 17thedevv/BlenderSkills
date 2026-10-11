---
name: live-broadcast-integration
description: Integrates a Warudo-tracked VRM avatar into OBS for webcam-based streaming, handling transparent capture, scene framing, hotkey expressions, and fallback behavior. Use after face tracking works.
---
# Live Broadcast Integration — Warudo to OBS

1. Confirm target is a desktop VTuber overlay/scene, not direct Blender viewport capture. Set face camera for readable anime eyes and mouth at realistic broadcast crop.
2. Produce a Warudo scene with stable camera, neutral transparent or chroma background as supported by the installed software, keybind expression toggles (happy/angry/sad/surprised), and optional secondary body idle; verify that expression layers do not block live lip sync/blink.
3. In OBS, select a capture method supported by installed Warudo and OBS (game/window capture and available transparency/chroma options); check actual alpha or chroma result before documenting success. Do not prescribe a transparency checkbox that does not exist in the installed version.
4. Test desktop content, overlays and face camera framing in both 16:9 stream and vertical 9:16 crop; save scene definitions/presets when software permits.
5. Verify webcam is only owned by the selected capture application; diagnose conflicts when other apps open the same camera. Check microphone visibility/access rights without requesting credentials.
6. Check idle/lost tracking behavior, tracking restart, head motion while reading a screen, and microphone lip sync fallback. Use real runtime and OBS observations; if unavailable, mark NOT TESTED.
7. Smoke test 10 minutes while OBS records (recording only if authorized by user). Profile render/render+encoding FPS and memory; keep low-cost fallback settings as documented in `docs/PERFORMANCE.md`.

**Exit:** OBS scene setup documentation, short real capture or screenshots if available, and logged setup/status.
