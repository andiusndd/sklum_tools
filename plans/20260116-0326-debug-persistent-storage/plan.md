# Debug Plan: Persistent Storage Failure

## 1. Problem
- User reports that "it still doesn't work" (key not persisting) despite the new Global Storage logic.

## 2. Hypotheses
1.  **Callbacks Not Firing**: `AddonPreferences.update` method might only fire when user *manually* edits the field, not when code sets it?
    - *Correction*: `update` callbacks in `bpy.props` DO fire on UI edits.
2.  **Startup Timing**: `auto_activate_license` runs on a timer. Maybe `global_storage` fails to read file?
3.  **Path Issues**: `Path.home()` on Windows might be returning something unexpected for this user (e.g., OneDrive mapping).
4.  **Silent Failures**: The `try...except` blocks in `global_storage.py` are printing to console (which user doesn't see). We need LOGS.

## 3. Action Plan
1.  **Add Logging**: Sprinkle `driver` level logs into `global_storage.py` and `preferences.py` to trace EXACTLY what's happening.
2.  **Verify Path**: Print the calculated Config Path to the console/log.
3.  **Force Save**: Add a manual "Save License Globally" button? No, that's bad UX.
4.  **Fix Strategy**:
    - Update `global_storage.py` to use `logger.info/error` instead of `print`.
    - Create a small test operator to "Show Config Path" for debugging.
    - Check if `license_key` property text is actually being passed to `save_license_key_global`.

## 4. Immediate Changes
- **Enhance Logging**: Make failures visible.
- **Double Check `update`**: Ensure the callback is actually registered properly.

## 5. Verification
- Ask user to open the Log File (using the button we fixed earlier!) and send us the content.
