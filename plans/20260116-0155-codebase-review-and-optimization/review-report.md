# Codebase Review Report: SKLUM Toolz

**Date:** 2026-01-16  
**Auditor:** Antigravity (AI Architect)

## Executive Summary
The codebase is well-structured and modular, using a "panel-based" directory organization. However, a critical persistence bug in the preferences module and architectural redundancies in property management were identified.

## Critical Issue: License Persistence
- **Root Cause:** In `core/preferences.py`, the `license_key` property uses `SKIP_SAVE`.
- **Impact:** Users must re-activate the addon every time Blender restarts.
- **Fix:** Remove `SKIP_SAVE` from the property options.

## Architectural Recommendations

### 1. Property Consolidation
- **Observation:** Over 20+ properties are attached directly to `bpy.types.Scene`.
- **Risk:** High chance of namespace collision and difficult state management.
- **Solution:** Wrap them in a `PropertyGroup` registered as `context.scene.sklum`.

### 2. License State Management
- **Observation:** License status is checked on every file load (`load_post`).
- **Optimization:** Cache the validation result in a runtime variable to avoid frequent server calls if the key hasn't changed.

### 3. Auto-Update Stability
- **Observation:** The update logic overwrites the active directory.
- **Improvement:** Implement a "stage-then-replace" logic with better error handling for locked files on Windows.

## Code Quality Metrics
- **Modularity:** ⭐⭐⭐⭐⭐ (Excellent folder structure)
- **Namespacing:** ⭐⭐⭐ (Good prefixes, but needs grouping)
- **Error Handling:** ⭐⭐⭐⭐ (Robust `try-except` blocks in key areas)
- **DRY Principle:** ⭐⭐⭐ (Redundant properties in `core` vs `panels`)

## Next Steps
1. Execute **Phase 1** of the optimization plan (Persistence Fix).
2. Refactor UI calls to use the new PropertyGroup structure.
3. Consolidate license logic into a dedicated manager class.

---
**Unresolved Questions:**
- Are there any specific firewall/proxy settings users might encounter that we should handle in `requests` calls?
- Should we implement an "Offline Mode" for validated licenses that lasts for N days?
