# Brainstorming Report: Persistent Update Failure (WinError 5)

## 1. Problem Diagnosis
- **Error**: `[WinError 5] Access is denied` when renaming `sklum_tools` -> `.sklum_tools.~temp~`.
- **Context**: This occurs during Blender's internal extension update process.
- **Root Cause**: **File Locking**. Windows prevents renaming a directory if any file inside it is open by a process.
- **The Culprit**: The `core.logger` initializes a `logging.FileHandler` that writes to `.../sklum_tools/logs/sklum_tools.log`. This file remains open as long as the addon is loaded. Blender tries to rename the folder *before* fully unloading/releasing the Python resources, or perhaps the unload sequence didn't explicitly close the handler.

## 2. Proposed Solutions

### Option A: Clean Shutdown (The "Correct" Way)
- **Concept**: Implement a `shutdown()` method in `SKLUM_Logger` that closes all handlers. Call this method in `__init__.py`'s `unregister()`.
- **Pros**: Keeps logs self-contained.
- **Cons**: Relies on Blender calling `unregister()` *before* failing the rename operation. If Blender's architecture attempts rename *before* full unload, this fails.

### Option B: External Logs (The "Robust" Way) - **RECOMMENDED**
- **Concept**: Move the log file *outside* the addon directory. Use the system temporary directory (`%TEMP%`).
- **Pros**: 
  - **Zero Lock Risk**: The addon folder has no open files.
  - **Permission Safe**: `%TEMP%` is always writable.
  - **Clean Updates**: Deleting/Renaming the addon folder is trivial.
- **Cons**: Logs are slightly harder to find (but we have an "Open Log" button in the UI anyway).

### Option C: No File Logging
- **Concept**: Only log to console.
- **Pros**: Simple.
- **Cons**: debugging hard for end-users.

## 3. Final Recommendation: Option B + A
We will move the log file to the system temp directory **AND** implement a proper shutdown cleanup. This guarantees the folder is never locked.

### Implementation Plan
1.  **Modify `core/logger.py`**:
    - Change `log_dir` to `tempfile.gettempdir()`.
    - Add `close()` method to release handlers.
2.  **Modify `__init__.py`**:
    - Import logger and call `close()` in `unregister()`.

## 4. Next Steps
- Execute `@/plan-hard` to detail the file changes.
- Execute `@/fix-hard` to apply.
