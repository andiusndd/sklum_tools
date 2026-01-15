# Plan: Persistent License Storage (Global)

## Context
Ref: [Research Report](../reports/research-persistent-storage.md).
We need to store the license key in the user's home directory (`~/.sklum_tools/config.json`) so it survives Blender updates, uninstalls, and version changes.

## Phase 1: Storage Logic (`core/global_storage.py`)
- **New File**: Create `core/global_storage.py`.
- **Functions**:
  - `get_storage_path()`: Return `Path.home() / .sklum_tools / config.json`.
  - `save_license_key(key)`: Save key to JSON.
  - `load_license_key()`: Load key from JSON.

## Phase 2: Preference Sync (`core/preferences.py`)
- **Action**:
  - Add an `update` callback to `license_key` property.
  - Callback: `save_license_key(self.license_key)`.
  - On `register()` (or module load?): We can't easily hook `__init__` of `AddonPreferences` in a way that modifies the property definition default.
  - **Better Strategy**: Use `bpy.app.handlers.load_post` or the existing `auto_activate_license` in `license_logic.py` to **PULL** the key from global storage into preferences if the preference is empty.

## Phase 3: Startup Logic (`core/license_logic.py`)
- **Action**:
  - Modify `auto_activate_license`:
    1. Check `prefs.license_key`.
    2. If empty, check `load_license_key()`.
    3. If found globally, update `prefs.license_key` (and `save_preferences`?).
    4. Proceed with validation.

## Success Criteria
1. Install Addon -> Enter Key -> Key saved to `~/.sklum_tools/config.json`.
2. Delete Addon -> Reinstall Addon -> Start Blender -> Key automatically populated in Preferences and Activated.

## Risks
- **WinError**: None expected in User Home.
- **Race Condition**: `auto_activate_license` runs on timer, so Blender is fully loaded. Safe to modify prefs.

## Implementation Steps
1. Create `core/global_storage.py`.
2. Update `core/preferences.py` (add update callback).
3. Update `core/license_logic.py` (add sync logic).
