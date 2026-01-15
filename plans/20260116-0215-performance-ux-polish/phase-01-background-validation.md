# Phase 01: Background Validation & Caching

## Context
- **Reference Plan:** [plan.md](./plan.md)
- **Goal:** Make the license check "invisible" and non-blocking.

## Overview
- **Date:** 2026-01-16
- **Description:** Implement background threading and memoization for licenses.
- **Priority:** HIGH
- **Implementation Status:** PENDING
- **Review Status:** PENDING

## Key Insights
- `subprocess` and `requests` are the bottlenecks.
- Blender 4.2+ handles timers smoothly for polling background threads.

## Requirements
- Background validation must not crash Blender if the thread fails.
- The UI must reflect a "Validating..." state if the user manually re-checks.
- Caching must survive a single session (Blender restart) but expire after 24 hours.

## Architecture
1. **Memoization**: `_cached_hwid` variable in `core/license_logic.py`.
2. **Threading**: Use `threading.Thread` for the POST request.
3. **Queue/State**: Store the validation result in a shared dictionary/object.
4. **Timer**: `auto_activate_license` will trigger a timer that updates the scene property once the thread finishes.

## Related code files
- `core/license_logic.py`
- `__init__.py`
- `panel_version_info/panel.py`

## Implementation Steps
1. **Global Cache for HWID**: Use a simple global variable to store the ID after first fetch.
2. **Async Validation Wrapper**: Create a function that runs `validate_license` in a thread.
3. **Timer-based Polling**: Add a Blender timer to check for thread completion and update `scene.sklum.license_active`.
4. **Persistent Cache**: Store the last successful validation timestamp in `preferences.license_last_validated`.

## Success Criteria
- Startup `load_post` takes < 0.1s regardless of server response speed.
- Clicking "Activate" shows an immediate "Kích Hoạt..." status without freezing the cursor.

## Security Considerations
- Ensure the locally cached validation timestamp is encrypted or at least compared against the server key on expiry.
