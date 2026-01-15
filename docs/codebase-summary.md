# Codebase Summary: SKLUM Tools

## 1. Directory Structure

- `__init__.py`: Root entry point. Handles lazy module dispatch and auto-licensing.
- `core/`: Global foundation.
    - `logger.py`: Centralized logging.
    - `license_logic.py`: Async DRM and HWID fetch.
    - `checker_logic.py`: Low-level mesh validation algorithms.
    - `utils.py`: Update logic and shared helpers.
- `panel_checker_tools/`: The primary "Check All" interface.
- `panel_auto_rename/`: CSV-driven naming system.
- `panel_import_export/`: GLB/FBX export and cleanup.
- `panel_jpg_converter/`: PNG to JPG optimization.
- `panel_object_setting/`: Viewport and pivot management.
- `panel_version_info/`: Lifecycle management (Update/License).
- `server_backend/`: Validation logic for the Vercel API.

## 2. Key Data Models

### `SKLUM_SceneSettings` (`core/properties.py`)
Centralized PointerProperty on `bpy.types.Scene`. Holds:
- `license_active`, `license_message`.
- Expansion states for UI panels.
- Aggregated check results.

### `CheckResult` (`core/checker_logic.py`)
Dataclass for check outputs:
- `status`: Pass/Fail.
- `message`: User-friendly status.
- `failed_objects`: List of problematic mesh names.

## 3. Communication Patterns
- **Internal**: Panels trigger Operators which call `core` functions.
- **External**: `license_logic` communicates with a Vercel-hosted API via `requests`.
- **Feedback**: Operators use `window_manager` for progress and `logger` for persistent logs.
