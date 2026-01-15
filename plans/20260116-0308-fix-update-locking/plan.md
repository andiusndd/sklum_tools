# Plan: Fix Update Locking (WinError 5)

## Context
- **Issue**: Updates fail with `[WinError 5]` because `logging.FileHandler` locks the addon folder.
- **Goal**: Move logs to `%TEMP%` and ensure handlers are closed on unregister.
- **Reference**: [Brainstorm Report](../reports/brainstorm-20260116-winerror-5-logs.md)

## Implementation Steps

### Phase 1: Relocate Logs
- **File**: `core/logger.py`
- **Action**: 
    - Import `tempfile`.
    - Change path to `os.path.join(tempfile.gettempdir(), "SKLUM_Logs")`.
    - Implement `shutdown()` method to `close()` and `removeHandler()` for file handlers.

### Phase 2: Cleanup on Unregister
- **File**: `__init__.py`
- **Action**:
    - Update `unregister()` to import `core.logger` and call `logger.shutdown()`.

### Phase 3: Verify Export
- **File**: `_export_FINAL_HOTFIX.py` (or create new)
- **Action**: Ensure this creates a valid package.

## Success Criteria
- Logs appear in `%TEMP%/SKLUM_Logs/`.
- `SKLUMToolz` folder can be renamed/deleted manually while Blender is running (after unregister).
