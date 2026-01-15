# System Architecture: SKLUM Tools

## 1. High-Level Overview
SKLUM Tools is a modular Blender addon. It separates UI (Panels), Logic (Operators), and Data (Properties) following a model-view-controller (MVC) inspiration, adapted for the Blender API.

## 2. Core Components

### 2.1 The Registration Engine
The root `__init__.py` acts as the entry point. It uses a **Lazy Dispatch pattern**:
1. Checks for license validity (using 24h cache).
2. Dynamically imports sub-packages (`core`, `panel_checker_tools`, etc.).
3. Calls `register()` on each.

### 2.2 Async License System
Designed for performance and compliance:
- `validate_license_async`: Spawns a background thread.
- `bpy.app.timers`: Polls the thread for results.
- Persistent Cache: Stores validation in `AddonPreferences` to bypass network on session restart.

### 2.3 Atomic Update Mechanism
Bypasses Windows file locks (`WinError 32`):
- Stage: Extract new version to temp.
- Swap: Rename current dir to `SKLUMToolz_old` $\rightarrow$ Move new version to original path.
- Cleanup: Try to delete `_old` dir (fails gracefully).

### 2.4 Checker Framework
Centralized in `core/checker_logic.py`:
- Pure Python functions with no UI code.
- Returns structured `CheckResult` objects.
- Allows the "Check All" operator to aggregate multiple checks efficiently.

## 3. Data Flow
1. **User Interaction**: User clicks a button in a Panel.
2. **Operator Execution**: Operator calls a function in `core`.
3. **Internal Processing**: Logic uses `constants.py` and returns data.
4. **State Update**: Result is written to `bpy.context.scene.sklum`.
5. **UI Refresh**: Blender's draw loop updates the panel based on the new property state.
