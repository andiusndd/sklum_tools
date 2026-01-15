# Implementation Plan - Persistent License Storage

Refactor the license system to store the activation key in `AddonPreferences` so it persists across Blender sessions.

## User Requirements
- License status/key must not be lost when restarting Blender.
- Auto-activation on startup if a key is already stored.

## Proposed Changes

### 1. New File: `preferences.py`
Create a new file `preferences.py` in the root of the addon.
- Define `SKLUM_Preferences(bpy.types.AddonPreferences)`.
- Add `bl_idname = __package__`.
- Add `license_key: StringProperty(name="License Key", subtype='PASSWORD')`.
- Implement `draw` method (optional, just to show key is stored).

### 2. Update `__init__.py`
- Import `preferences`.
- Add `preferences` to `modules` list for registration.
- Import `bpy` and `from bpy.app.handlers import persistent`.
- Define `auto_activate_license(dummy)` function:
    - Get `prefs = bpy.context.preferences.addons[__name__].preferences`.
    - If `prefs.license_key`:
        - Call `validate_license(prefs.license_key)`.
        - Update `bpy.context.scene.sklum_license_active` result.
- In `register()`:
    - Register `SKLUM_Preferences`.
    - Append `auto_activate_license` to `bpy.app.handlers.load_post`.

### 3. Update `panel_checker_tools/license_manager/operator.py`
- **Activate Operator**:
    - On success (`'License Valid'` / `'Activated successfully'`), save the key to preferences.
    - `context.preferences.addons[__package__.split('.')[0]].preferences.license_key = self.key` (Need to handle package name carefully).
- **Deactivate Operator**:
    - Clear the key from preferences.
    - `context.preferences.addons[__package__.split('.')[0]].preferences.license_key = ""`

## Verification Plan
1. **Manual Test**:
    - Install updated addon.
    - Enter license key -> Activate.
    - Verify key is stored (check User Preferences > Addons).
    - Restart Blender.
    - Verify License is still Active (Auto-check worked).
2. **Deactivation Test**:
    - Click Deactivate.
    - Restart Blender.
    - Verify License is NOT Active.
