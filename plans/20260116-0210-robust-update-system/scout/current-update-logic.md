# Scout Report: Current Update & Logging State

## Files Analyzed
- `core/utils.py`: Contains `check_for_update` and `download_and_install_update`.
- `panel_version_info/panel.py`: UI for triggering updates.
- Multiple modules using `print()` for errors.

## Current Update Logic
- Downloads ZIP to a temp file.
- Extracts to a temp directory.
- Deletes items in `addon_dir` using `shutil.rmtree` (no retry) or `shutil.copytree` (brittle).
- Uses `safe_remove` for cleanup of temp files only.

## Performance/Stability Issues
- **Brittle Folder Deletion**: `shutil.rmtree(d)` in line 184 of `core/utils.py` will crash if any file is locked, failing the entire update.
- **Silent Failures**: Errors are printed to console but not easily visible to users if they don't have the console open.
- **Inconsistent logging**: Some errors use `print()`, others `self.report()`, others are swallowed.

## Actionable Targets
- Move update logic to a "stage-then-swap" approach.
- Replace `print()` calls with a new `logger` module.
- Add a persistent log file.
