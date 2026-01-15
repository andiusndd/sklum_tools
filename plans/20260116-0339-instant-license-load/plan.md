# Plan: Instant License Load & Async Verify

## Context
User complains that license load is slow/flaky. We need "Instant Active" UX.
Ref: Previous Brainstorming.

## 1. Load Strategy
- **File**: `core/license_logic.py` & `__init__.py`.
- **Change**: 
    - Move `load_license_key_global()` call to `auto_activate_license` TOP (sync part).
    - Or better, call it inside `register()` of `__init__.py` to preload the environment? 
    - *Decision*: Keep it in `auto_activate_license` but ensure it runs *immediately* on first timer tick (0.0s delay?), and updates UI properties *before* starting the async thread.

## 2. UI Feedback
- **File**: `panel_version_info/panel.py` (and others).
- **Change**: 
    - If `license_key` is present but `license_active` is False:
        - Check `license_message`. If empty -> Set to "Initializing...".
        - Interpret "Initializing" or "Validating" as YELLOW state (Warning Icon), not RED (Error Icon).

## 3. Implementation Steps

### Step 1: Optimize `auto_activate_license` in `core/license_logic.py`
- Read Global Key immediately.
- If found:
    - Set `scene.sklum.license_key`.
    - Set `scene.sklum.license_message = "Validating..."` (Yellow state).
    - **THEN** start async thread.
- If not found:
    - Exit (Red state).

### Step 2: Update UI in `panel_version_info/panel.py`
- Logic:
    - `if not license_active`:
        - `if message == "Validating..."`: Show Yellow "Đang kiểm tra..." box.
        - `else`: Show Red "Chưa kích hoạt" box.

## 4. Risks
- **Race Condition**: Setting `scene` properties during startup *might* fail if Context isn't fully ready. `bpy.app.timers` usually guarantees Context is ready.
- **Update Loop**: Setting key might trigger `update` callback which writes back to global. This is fine (idempotent code).

## 5. Execution
- Execute `@/fix-hard` directly.
