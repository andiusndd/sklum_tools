# Phase 1: Persistence & Property Consolidation

## Context
The addon currently suffers from a persistence issue where the license key is lost on restart. Additionally, scene properties are scattered, cluttering the `bpy.types.Scene` namespace.

## Overview
- **Date:** 2026-01-16
- **Priority:** CRITICAL (Persistence fix)
- **Status:** Completed

## Key Insights
- `SKIP_SAVE` in `core/preferences.py` is the root cause of license loss.
- Centralizing properties into a `PropertyGroup` improves maintainability and tab-completion.

## Requirements
- Fix license persistence by modifying `AddonPreferences`.
- Group all `sklum_` scene properties into a single `PointerProperty`.

## Related Code Files
- `core/preferences.py`
- `panel_checker_tools/properties.py`
- `__init__.py`

## Implementation Steps
1.  **Modify `core/preferences.py`**:
    - Remove `SKIP_SAVE` from `license_key`.
    - Ensure `bl_idname` is strictly set to the top-level package name.
2.  **Refactor `panel_checker_tools/properties.py`**:
    - Create `SKLUM_SceneSettings` PropertyGroup.
    - Move all individual `sklum_` properties into this group.
    - Register it as `context.scene.sklum`.
3.  **Update UI & Operators**:
    - Search and replace all `scene.sklum_property` with `scene.sklum.property`.
4.  **Test Persistence**:
    - Activate license, restart Blender, verify it's still active.

## Success Criteria
- [ ] License key persists after closing and reopening Blender.
- [ ] Addon loads without property registration warnings.
- [ ] UI reflects accurate state from the consolidated PropertyGroup.
