# SKLUM Tools – Blender Add-on

**Author:** AndiuS  
**Version:** 2.8.0  
**Blender:** 4.2.0+  
**Source:** [https://github.com/andiusndd/sklum_tools](https://github.com/andiusndd/sklum_tools)

SKLUM Tools provides a suite of Quality Assurance (QA) utilities, automated renaming, and optimized import/export workflows for professional 3D production pipelines.

---

## 📚 Documentation
Please refer to the detailed documentation in the `docs/` folder:
- [📖 Project Overview & PDR](docs/project-overview-pdr.md)
- [🧩 Codebase Summary](docs/codebase-summary.md)
- [🏗️ System Architecture](docs/system-architecture.md)
- [📏 Code Standards](docs/code-standards.md)

---

## 🚀 Key Features
*   **Check All:** Comprehensive QA for UVs, Seams/Sharps, Color Space, Modifiers, and Vertex Groups with real-time progress bars and structured reporting.
*   **License System:** Non-blocking background hardware ID (HWID) validation with 24-hour persistence for seamless workflows.
*   **Auto Rename:** Batch rename Objects/Materials/Textures via CSV rules (IDP) with powerful Preset support.
*   **Robust Updates:** Atomic "Rename-Swap" update mechanism designed to bypass Windows file locks (`WinError 32`).
*   **Centralized Logging:** Unified logging to both the Blender System Console and a persistent disk file for easier support.
*   **Checker Tools:**
    *   **Color Space:** Auto-fix Texture Color Space (sRGB/Non-Color).
    *   **Active Point:** Origin normalization & Quick Group-to-Empty.
    *   **Grid Checker:** Detect unwanted Triangles/N-gons.
*   **Import/Export:** Optimized FBX/GLB export with compression and texture customization.
*   **JPG Converter:** Batch convert PNG textures to JPG.

## 📥 Installation
1.  Download the `.zip` file from Releases.
2.  Open Blender > `Edit → Preferences → Add-ons` > `Install...` and select the `.zip`.
3.  Search for and enable **SKLUM Tools**.
4.  **Enter your License Key** in the sidebar to activate the tools.

## 🛠️ Development
See [Codebase Summary](docs/codebase-summary.md) for architecture details.
- **`core/`**: Shared logic, Logging, DRM, and global properties.
- **`panel_*/`**: Modular UI panels for specific feature groups (Lazy loaded).
- **`server_backend/`**: Vercel/Supabase backend code for license validation.

## 📜 Update Log
See detailed changes in [UPDATE-LOG.md](UPDATE-LOG.md).
