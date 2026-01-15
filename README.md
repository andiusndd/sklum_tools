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
- [📁 Project Structure](STRUCTURE.md) (Legacy)

---

## 🚀 Key Features
*   **Check All:** Comprehensive QA for UVs, Seams/Sharps, Color Space, Modifiers, and Vertex Groups with structured reporting.
*   **License System:** Secure device-locking DRM to protect IP.
*   **Auto Rename:** Batch rename Objects/Materials/Textures via CSV rules (IDP) with powerful Preset support.
*   **Checker Tools:**
    *   **Color Space:** Auto-fix Texture Color Space (sRGB/Non-Color).
    *   **Active Point:** Origin normalization & Quick Group-to-Empty.
    *   **Grid Checker:** Detect unwanted Triangles/N-gons.
*   **Import/Export:** 
    *   Optimized FBX/GLB export.
    *   Draco Compression & Texture format customization.
    *   Pack/Unpack & Data Purge tools.
*   **JPG Converter:** Batch convert PNG textures to JPG (Requires Pillow).

## 📥 Installation
1.  Download the `.zip` file from Releases.
2.  Open Blender > `Edit → Preferences → Add-ons` > `Install...` and select the `.zip`.
3.  Search for and enable **SKLUM Tools**.
4.  **Enter your License Key** in the sidebar to activate the tools.

## 🛠️ Development
See [Codebase Summary](docs/codebase-summary.md) for architecture details.
- **`core/`**: Shared logic, DRM, and global properties.
- **`panel_*/`**: Modular UI panels for specific feature groups.
- **`server_backend/`**: Vercel/Supabase backend code (not included in Addon zip).

## 📜 Update Log
See detailed changes in [update-log.md](update-log.md).
