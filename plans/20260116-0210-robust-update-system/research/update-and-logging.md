# Research Report: Robust Updates & Logging for Blender Addons

## Topics Covered
1. **Windows File Locks (`WinError 32`)**: Strategies for replacing files while Blender is running.
2. **Centralized Logging**: Implementing a persistent logging system with UI feedback.

## Insights
### Update Stability
- **Atomic Swap**: Instead of deleting and copying file-by-file, rename the existing addon folder to `*.old` and move the new version into place. This is more likely to succeed even if some files are partially locked for reading.
- **Retry Mechanism**: The current `safe_remove` is good but should be integrated into a higher-level `safe_move` or `safe_replace` utility.
- **Cleanup**: `*.old` directories should be cleaned up on the *next* startup to ensure no locks remain.

### Centralized Logging
- **Standard Library**: `logging` is the standard. A custom logger `SKLUM` should be configured.
- **Handlers**:
    - `StreamHandler`: Logs to System Console.
    - `FileHandler`: Logs to `{addon_dir}/logs/sklum.log`.
- **UI Integration**: Since Blender doesn't have a built-in log viewer widget, we can use a `CollectionProperty` to store recent log messages or simply show the "Last Error" in the UI.

## Recommendations
- Create `core/logger.py` to centralize all messaging.
- Refactor `download_and_install_update` to use a "Stage -> Swap -> Cleanup" workflow.
- Add a "Log Viewer" operator to open the log file in the system's default text editor.

## Unresolved Questions
- Should we use a custom UI list for logs inside Blender, or just link to the log file? (Recommendation: Start with link to file for simplicity).
