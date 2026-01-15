# Phase 1: Client-Side Logic (HWID & UI)

## Context
We need the Addon to be able to identify the computer it is running on uniquely and provide a UI for the user to input their License Key.

## Key Insights
- **Windows HWID**: `wmic csproduct get uuid` is the standard way to get a motherboard UUID on Windows. It is persistent across re-installs.
- **Storage**: The License Key should be stored in `bpy.context.preferences.addons[__name__].preferences`.

## Implementation Steps
1.  **Create `core/license_logic.py`**:
    -   Function `get_machine_id()`: Executes `wmic` command safely.
    -   Function `validate_license(key)`: Sends HTTP request to Server (Mocked for now).
    -   *Constraint*: Do NOT require email input in UI. Only License Key.
2.  **Update `preferences.py`**:
    -   Add `license_key` (StringProperty, subtype='PASSWORD').
    -   Add `activate_button` operator.
3.  **UI Updates**:
    -   Show "Unregistered" status in the Panel if not activated.
    -   Block key operators (like Auto-Rename or Check) if `is_active` is False.

## Todo List
- [x] Implement `get_machine_id` in `core/utils.py` or new `core/license.py`.
- [x] Create `SKLUM_OT_activate_license` operator.
- [x] Add License Key field to Addon Preferences.
- [x] Add "Gatekeeper" check to `sklum.check_all`.
