# Phase 02: Checker Optimization & Progress Indicators

## Context
- **Reference Plan:** [plan.md](./plan.md)
- **Goal:** Improve user feedback during batch operations.

## Overview
- **Date:** 2026-01-16
- **Description:** Implement `window_manager` progress indicators and optimize mesh check loops.
- **Priority:** MEDIUM
- **Implementation Status:** PENDING

## Implementation Steps
1. **Progress Wrapper**: Create a context manager or helper for `wm.progress_begin/update/end`.
2. **Inject Progress into `SKLUM_OT_check_all`**: Count total checks and update the bar after each one.
3. **Optimizing mesh checks**: In `checker_logic.py`, ensure we are not iterating over the same objects multiple times inside sub-functions if they can be combined.

## Success Criteria
- Running "Check All" on a heavy scene displays a progress bar in the bottom status bar and mouse cursor changes to a loading icon.
