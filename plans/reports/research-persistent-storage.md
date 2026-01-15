# Research Report: Persistent License Storage 3.0

## 1. Context & Problem
- **Legacy Issue**: `AddonPreferences` are stored in Blender's `userpref.blend`.
- **v4.2+ Risk**: In the new Extension system, uninstalling/removing an extension may purge its preferences.
- **Goal**: "Store Once, Run Anywhere". The license key must survive:
  1. Addon Updates (already covered, but robustness is key).
  2. Addon Uninstalls/Reinstalls.
  3. Blender Version Migrations (e.g., 4.2 -> 4.3).

## 2. Research Findings
- **Blender Folders**:
  - `bpy.utils.user_resource('CONFIG')` -> `%APPDATA%\Blender Foundation\Blender\4.2\config`. (Version specific).
  - **NOT GOOD**. Data here dies when user installs Blender 4.3.
- **User Home (The Solution)**:
  - Path: `~/.sklum_tools/license.json` (Linux/Mac) or `%USERPROFILE%\.sklum_tools\license.json` (Windows).
  - **Pros**: 
    - Globally accessible by ALL Blender versions.
    - Completely independent of Addon lifecycle.
    - Python standard lib (`pathlib`) makes this trivial.
- **Implementation Pattern**: "Sync-on-Load".
  - **Start**: Addon checks global file -> Fills Preferences.
  - **Input**: User types key -> Saves to global file.

## 3. Implementation Plan
### Phase 1: Create `core/global_storage.py`
- Define `get_storage_path()`: Uses `Path.home() / ".sklum_tools"`.
- Define `save_global_key(key)`: Writes JSON.
- Define `load_global_key()`: Reads JSON.

### Phase 2: Integrate with `core/preferences.py`
- On `register()` of preferences (or `__init__`), load the global key.
- Update `license_key` property to use an `update=` callback that saves to global storage.
- **Crucial**: Ensure we don't create infinite loops (Load -> Set Prop -> Update Callback -> Save -> ...). The `update` callback only triggers on user interaction or explicit set, which is fine, but we should check `if new_key != stored_key`.

### Phase 3: Integrate with `core/license_logic.py`
- "Auto-Activate" needs to look at *both* Preferences (priority) and Global Storage (fallback/recovery).
- Actually, if we sync properly in Phase 2, Preferences *will* have the key on startup, so `license_logic` doesn't need to change much, just rely on the (now correctly populated) Preferences.

## 4. Risks & Mitigations
- **Permission Error**: Writing to User Home is generally safe.
- **Multiple Blenders**: If two Blender instances try to write simultaneously? JSON write is atomic enough for this low-frequency event.

## 5. Next Steps
- Execute `@/plan-hard` for file specs.
- Execute `@/fix-hard` to implementing.
