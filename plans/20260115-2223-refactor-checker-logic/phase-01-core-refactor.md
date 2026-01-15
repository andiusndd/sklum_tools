# Phase 1: Core Logic Refactor

## Context
Currently, check logic is embedded in `execute()` methods and returns formatted strings. This makes it hard to reuse or reliably parse results.

## Overview
- **Date**: 2026-01-15
- **Description**: Extract logic into `core/checker_logic.py`. Define `CheckResult` dataclass.
- **Priority**: High

## Key Insights
- Logic should be pure python functions where possible (accepting `bpy.types.Object` or `bpy.types.Scene`), returning data objects.
- `CheckResult` should contain: `status` (bool), `message` (str), `failed_objects` (list of names/refs).

## Architecture
- **New File**: `core/checker_logic.py`
  - `class CheckResult`
  - `def check_uv_map(objects) -> CheckResult`
  - `def check_texture_pack(materials) -> CheckResult`
  - ... other checks ...

## Implementation Steps
1. Create `core/checker_logic.py`.
2. Define `CheckResult` class.
3. Move UV check logic from `check_all` to `check_uv_map`.
4. Move Texture Pack check logic to `check_texture_pack`.
5. Move other checks (Modifier, Vertex Group, etc.) similarly.
6. Ensure original operators import and use these new functions (temporarily formatting the output back to string to keep UI working until Phase 2).

## Todo List
- [ ] Create `core/checker_logic.py`
- [ ] Implement `check_uv_map`
- [ ] Implement `check_texture_pack`
- [ ] Implement `check_modifiers`
- [ ] Implement `check_vertex_groups`
- [ ] Verify `check_all` operator still works (using adapters).

## Success Criteria
- All check logic exists in `core/checker_logic.py`.
- `check_all` operator code is reduced to calling these functions.
