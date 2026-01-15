# Plan: Force UI Redraw on Activation

## Context
User reports UI doesn't update (change from Yellow to Green) unless mouse moves.
Fix: Explicitly force a Blender UI redraw when the async activation completes.

## 1. Logic
- **File**: `core/license_logic.py`.
- **Target**: `_poll_activation_result` function.
- **Change**: Loop through `bpy.context.window_manager.windows` and call `tag_redraw()` on all areas.

## 2. Risk
- **None**: This is standard Blender API usage for async updates.

## 3. Execution
- Patch `core/license_logic.py`.
