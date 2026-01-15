# Phase 02: Resilient Update Refactor

## Context
- **Reference Plan:** [plan.md](./plan.md)
- **Goal:** Resolve `WinError 32` failures during auto-updates.

## Overview
- **Date:** 2026-01-16
- **Implementation Status:** PENDING
- **Priority:** HIGH

## Key Insights
- Windows "Access Denied" often occurs when `shutil.rmtree` tries to delete a folder while a file is even momentarily indexed or used by another Blender instance/process.
- **Rename-and-Orphan Trick**: Renaming a folder is generally faster and allowed more often than deletion. Rename the addon folder to `SKLUMToolz_old`, place the new `SKLUMToolz` folder, and try to delete `_old`. If deletion fails, leave it and mark for future cleanup.

## Requirements
- No partial updates (either new version is fully in place, or nothing changes).
- Robust retries for all file system moves.
- Clear user feedback if a restart is required but the update "staged" successfully.

## Architecture
1. **Download**: To temp ZIP.
2. **Extract**: To temp dir.
3. **Stage**: Verify new folder integrity.
4. **Swap**: 
   - Rename `current_addon_dir` -> `temp_old_dir`.
   - Move `new_addon_dir` -> `current_addon_dir`.
5. **Cleanup**: Attempt to delete `temp_old_dir`.

## Related code files
- `core/utils.py`: `download_and_install_update` refactor.

## Implementation Steps
1. Enhance `safe_remove` with better exception handling.
2. Implement `swap_addon_folders` utility.
3. Wrap the core of `download_and_install_update` in the new swap logic.
4. Test "Force Fail" scenarios (simulated lock).

## Success Criteria
- Update completes even if a file in the addon directory is "Read-Only" or temporarily "Busy".
- No "AttributeError" or "ModuleNotFound" errors after a partial fail.
