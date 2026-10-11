# Base Mesh Strategy & Provenance Audit Report

## 1. Candidate Asset Evaluation

### Candidate A: `Aplaybox_Hsin.zip` (Workspace Candidate)
- **File Name**: `Aplaybox_Hsin.zip` (`【Aplaybox】 Hsin.blend`, 73.2 MB + 59 textures)
- **Origin & Creator**: Kuro Games / Wuthering Waves (*Rover / Xin / Hsin* official game model), distributed on Aplaybox (模之屋).
- **License & Legal Constraints**:
  - **Strictly Non-Commercial Fan Work Only** (MMD / non-monetized video clips).
  - Copyright belongs exclusively to Kuro Games.
  - Commercial VTuber streaming, monetization, rebranding as an "original VTuber", and redistribution are **strictly forbidden** by Kuro Games End-User License Agreement and Aplaybox Terms of Service.
- **Topology & Features**: High-quality AAA game mesh, but violates core project constraints.
- **Audit Finding**: **DISQUALIFIED / REJECTED (CRITICAL LEGAL BLOCKER)**. Using this asset violates Rule 2 ("original Japanese-anime-style female VTuber"), Rule 4 ("All external assets require verifiable provenance/permission for modification and commercial streaming/redistribution"), and `docs/QUALITY_RUBRIC.md` disqualifiers.

---

### Candidate B: VRoid Studio-Derived Anime Base Mesh (Recommended)
- **Origin & Creator**: Pixiv Inc. / VRoid Studio (exported as editable base mesh).
- **License & Legal Constraints**:
  - Commercial use permitted for streaming, broadcasting, and content creation.
  - Derivative works and modifications permitted.
  - Redistribution permitted when customized into an original character.
- **Topology & Features**:
  - Standard VRM 1.0 humanoid armature hierarchy (`hips`, `spine`, `chest`, `neck`, `head`, `leftEye`, `rightEye`).
  - Pre-aligned eye bone LookAt setup.
  - Standardized facial viseme topology and base blendshapes.
- **Audit Finding**: **RECOMMENDED BASE ROUTE**. Provides clean legal clearance, robust deformation loops, and standard VRM 1.0 compatibility while allowing full custom reshaping in Blender.

---

### Candidate C: Custom Blender Clean Quad Blockout (Alternative)
- **Origin & Creator**: Authored in Blender from 2D orthographic concept guides.
- **License & Legal Constraints**: 100% original IP, unrestricted commercial streaming and redistribution.
- **Topology & Features**: Custom quad topology with specialized edge loops for anime eyelids and mouth corners. Requires full manual rigging, weight painting, and blendshape authoring from scratch.
- **Audit Finding**: **VIABLE BESPOKE ROUTE**. Cleanest legal pedigree, but requires full manual rigging and blendshape sculpt passes.

---

## 2. Decision & Next Steps
1. **Preserve `Aplaybox_Hsin.zip`** untouched in root/source archive without modifying or presenting it as original work.
2. **Proceed with Candidate B or C** based on user confirmation.
