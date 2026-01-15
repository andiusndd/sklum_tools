# Phase 02: Modular Refactoring & Registration Optimization

## Context
- **Reference Plan:** [plan.md](./plan.md)
- **Dependencies:** [Phase 01: Persistence Cleanup](../20260116-0155-codebase-review-and-optimization/phase-01-persistence-cleanup.md) (Previously completed)

## Overview
- **Date:** 2026-01-16
- **Description:** Implement a standardized, robust registration system across all addon modules to improve performance and stability.
- **Priority:** HIGH
- **Implementation Status:** Completed
- **Review Status:** PENDING

## Key Insights
- **Top-level imports** are the primary cause of "partially initialized module" errors in Blender addons.
- **Inconsistent unregistration** leads to "restored settings" and corrupted UI states when reloading the addon.
- **Registration order** is critical: Core properties > Logic/Operators > UI Panels.

## Requirements
- Standardize all `__init__.py` files to use a consistent `register`/`unregister` pattern.
- Implement lazy loading for non-critical submodules.
- Ensure 100% clean unregistration (no orphans).

## Architecture
- **Centralized Registry**: Each sub-directory's `__init__.py` manages its own sub-modules.
- **Safe Dispatcher**: The root `__init__.py` dispatches calls to sub-packages.
- **Reversed Cleanup**: Unregistration always occurs in the exact inverse order of registration.

## Related code files
- `__init__.py` (Root)
- `core/__init__.py`
- `panel_checker_tools/__init__.py`
- `panel_auto_rename/__init__.py`
- `panel_import_export/__init__.py`
- `panel_jpg_converter/__init__.py`
- `panel_object_setting/__init__.py`
- `panel_version_info/__init__.py`

## Implementation Steps
1. **Standardize Sub-module Registration**:
   - Update `core/__init__.py` to use a safe loop with `hasattr(module, 'register')`.
   - Update `panel_checker_tools/__init__.py` similarly.
2. **Implement Lazy Imports**:
   - In sub-package `__init__.py` files, move submodule imports *inside* the `register()` and `unregister()` functions or maintain them in a local `modules` list that is only iterated during these calls.
3. **Refactor Root Registration**:
   - Enhance the root `__init__.py` to handle exceptions during registration more gracefully.
4. **Manual Validation**:
   - Install/Uninstall cycle in Blender.
   - Reload Scripts cycle (`F3` > "Reload Scripts").

## Todo list
- [ ] Refactor `core/__init__.py`
- [ ] Refactor `panel_checker_tools/__init__.py`
- [ ] Refactor `panel_auto_rename/__init__.py`
- [ ] Refactor `panel_import_export/__init__.py`
- [ ] Refactor `panel_jpg_converter/__init__.py`
- [ ] Refactor `panel_object_setting/__init__.py`
- [ ] Refactor `panel_version_info/__init__.py`
- [ ] Final root `__init__.py` update

## Success Criteria
- Addon registers without any "partially initialized" or "import" errors.
- Unregistering the addon removes all panels and properties.
- Reloading scripts doesn't duplicate UI elements.

## Risk Assessment
- **Risk**: Moving imports inside functions might hide syntax errors until runtime.
- **Mitigation**: Run a quick validation check using `python -m py_compile` or similar.

## Security Considerations
- Ensure no sensitive data is printed during registration (log levels).

## Next steps
- Proceed to Phase 3: Robust Update & Error Handling.
