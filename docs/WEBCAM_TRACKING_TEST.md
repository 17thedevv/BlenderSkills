# Webcam Tracking Live Acceptance Test — to be completed by real operator

**Runtime:** Warudo version TBD. **Tracking:** Built-in MediaPipe. **Target:** VRM 1.0. **Webcam:** TBD. **Operator approval:** PENDING.

> These are required manual/runtime tests. No test has been performed in this Skillpack authoring environment. Mark one of PASS/FAIL/NOT TESTED with actual evidence for each case.

| ID | Action | Expected visible result | Status | Evidence / observations |
|---|---|---|---|---|
| T01 | Camera neutral/calibration | Face/front stable, no permanent mouth opening | NOT TESTED | |
| T02 | Close both eyes; blink | Lids close fully without iris/eyelash clipping | NOT TESTED | |
| T03 | Smile and relax | Controllable expression, returns neutral | NOT TESTED | |
| T04 | Speak five distinct vowel-like sounds | Mouth movement follows speech reasonably, no snapping | NOT TESTED | |
| T05 | Head turn left/right ±20°, up/down ±15° | Head follows, no hair/clothing intersection | NOT TESTED | |
| T06 | Look left/right | Eyes track without pop-out or wrong direction | NOT TESTED | |
| T07 | Activate happiness via hotkey while talking | Mouth and blink remain reasonable according to configured overrides | NOT TESTED | |
| T08 | Cover camera then restore | Graceful neutral/idle fallback, recovery without manual reload when possible | NOT TESTED | |
| T09 | Warudo alone / Warudo+OBS / +game | Usable performance at target 30fps after measurement | NOT TESTED | |
| T10 | OBS 16:9 and portrait crop | Readable face, valid background extraction, audio synchronization | NOT TESTED | |
| T11 | 10-minute smoke test | No repeated tracking hang or unacceptable FPS/latency | NOT TESTED | |

**Notes:** Camera-based expressions can vary with lighting, calibration, distance, and occlusion. Record version and lighting; manual confirmation is required. Distinguish successful face tracking from complete full-body tracking (webcam alone does not guarantee it).
