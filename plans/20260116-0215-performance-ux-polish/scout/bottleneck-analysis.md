# Scout Report: Current Performance Bottlenecks

## Observed Locations
1. `core/license_logic.py:8`: `get_machine_id()` uses `subprocess` every call.
2. `core/license_logic.py:53`: `requests.post()` is synchronous and blocking.
3. `__init__.py:35`: `auto_activate_license` blocks startup with a network check.
4. `panel_checker_tools/check_all/operator.py`: Sequential execution of multiple mesh checks on large selections without progress feedback.

## Issues Identified
- **UI Hitching**: Fetching HWID causes a minor skip in UI frame rate.
- **Addon Lag**: Clicking "Kích Hoạt" makes Blender appear "Not Responding" for a few seconds.
- **Unnecessary Traffic**: Every file load triggers a server hit, increasing server load and slowing down the user.

## Actionable Targets
- [ ] Memoize `get_machine_id`.
- [ ] Implement local validation cache (TTL 24h).
- [ ] Thread the `requests` call in `validate_license`.
- [ ] Add `progress_begin/end` to `SKLUM_OT_check_all`.
