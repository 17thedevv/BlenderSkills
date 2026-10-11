---
name: character-director
description: Defines art direction, character identity, proportions, reference matching and staged approval for stylized anime 3D VTuber creation in Blender. Use before modeling and whenever design drifts.
---
# Character Director

**Inputs:** `config/character_brief.json`, any actual user concept images, user preferences, streaming crop, art style.

**Procedure**
1. Parse/validate brief; mark unspecified features as TBD, not invented requirements. Ask for missing identity/reference only when essential; propose a reversible aesthetic default otherwise.
2. Produce a one-page design sheet: clear silhouette at 128px, face/eye appeal targets, hair shape language, body proportions, color hierarchy (dominant / support / accent), outfit complexity budget.
3. Describe modeling priority: 70% of visual polish effort on face/hair/upper torso in the MVP; avoid details invisible at webcam size.
4. Identify 3 reference attributes to match and 3 no-go features (e.g. overly realistic nose, flat cylinders for hair, cluttered jewelry).
5. Pick checkpoints and artifact names for front, side, 3/4 and face close-up. Log concept status and get Gate A approval in `outputs/DELIVERY.md`.

**Rules:** A good concept image is not a finished 3D asset; user must approve the style. If concept images cannot be produced with available tools, request reference images; do not claim generation. Never clone protected 3D characters without permission.

**Exit artifacts:** `outputs/design/character_direction.md`, list of references/provenance, Gate A state.
