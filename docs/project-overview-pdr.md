# Project Overview & PDR: SKLUM Tools

## 1. Executive Summary
**SKLUM Tools** is a specialized Blender addon designed for 3D artists and production pipelines. Its primary purpose is to automate mesh validation, material standardization (IDP), and scene optimization to ensure assets are "production-ready" for real-time applications and high-quality rendering.

## 2. Product Development Requirements (PDR)

### 2.1 Target Audience
- 3D Artists (Mesh checking, UV validation).
- Technical Artists (Material standardization, color space management).
- Pipeline Engineers (Auto-renaming via CSV, batch export).

### 2.2 Core Modules
- **Registration & Modularity**: Lazy loading of sub-modules to prevent circular imports.
- **Licensing & DRM**: Non-blocking background hardware ID (HWID) validation with 24-hour persistence.
- **Checker Logic**: Automated checks for UVs, Hard Edges, Vertex Groups, and Material Properties.
- **Update System**: Resilient atomic "Rename-Swap" update mechanism for Windows.
- **Logging**: Centralized logging to both Blender console and local disk.

### 2.3 User Experience Goals
- No UI freezing during network operations.
- Clear visual feedback (Progress bars, Log access).
- One-click "Fix" operators for common mesh errors.

## 3. Key Differentiators
- **IDP Integration**: Support for CSV-driven object and material renaming.
- **Atomic Operations**: Update system that bypasses Windows file locks.
- **Performance-First**: Extensive use of memoization and background threading.
