# Plan: Robust Update System & Centralized Logging

## Overview
Implement a resilient update mechanism that survives Windows file locks and a centralized logging system to aid in debugging and user support.

## Context
- **Parent Plan:** [Phase 3 in review-and-optimization/plan.md](../20260116-0155-codebase-review-and-optimization/plan.md)
- **Status:** Planning

## Phases
1. **Centralized Logging Infrastructure**: Create `core/logger.py` and integrate it into `register()`.
2. **Resilient Update Logic**: Refactor `download_and_install_update` with a "rename-swap" strategy.
3. **UI Integration & Final Cleanup**: Add log viewing capabilities to the UI.

## Progress
- Total Progress: 0%

### [Phase 1: Logging Infrastructure](./phase-01-logging-infrastructure.md)
- [ ] Create `core/logger.py`.
- [ ] Initialize file and console handlers.
- [ ] Implement `sk_log(message, level='INFO')` wrapper.

### [Phase 2: Resilient Update Refactor](./phase-02-resilient-update.md)
- [ ] Implement `safe_move` and `atomic_replace`.
- [ ] Refactor `download_and_install_update` to use the new strategy.
- [ ] Add post-update "cleanup scheduled" flag.

### [Phase 3: UI & Validation](./phase-03-ui-and-validation.md)
- **Status:** Completed
- [x] Add "Open Log File" button to `panel_version_info`.
- [x] Test update on Windows with simulated file locks.
