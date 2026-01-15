# Phase 2: UI & Property Integration

## Context
After Phase 1, logic is clean but UI still relies on legacy string properties (`scene.sklum_*_check_result`). We need to modernize the data storage and UI rendering.

## Overview
- **Date**: 2026-01-15
- **Description**: Create structured properties for check results and update UI.
- **Priority**: Medium

## Key Insights
- We need a `PropertyGroup` to hold a single check result (status, message, list of failed objects).
- We need a `CollectionProperty` or fixed set of PointerProperties to hold all results.

## Architecture
- **`panel_checker_tools/properties.py`**:
  - `class SKLUM_CheckResultItem(PropertyGroup)`
  - `class SKLUM_CheckResults(PropertyGroup)` (Container for all checks)
- **`panel_checker_tools/panel.py`**:
  - Update `draw` to iterate over the structured data instead of parsing strings.

## Implementation Steps
1. Define `SKLUM_CheckResultItem` in `properties.py` (fields: `name`, `status` (bool), `message`, `object_count`).
2. Add `sklum_check_results` (CollectionProperty) to Scene.
3. Update `check_all` operator to populate this CollectionProperty instead of setting string properties.
4. Update `panel.py` to draw from `scene.sklum_check_results`.
5. Remove old string properties (`scene.sklum_uvmap_check_result`, etc.).

## Todo List
- [ ] Define `SKLUM_CheckResultItem`
- [ ] Register new properties
- [ ] Update `check_all` to populate new properties
- [ ] Update `panel.py` layout
- [ ] Cleanup old properties

## Success Criteria
- UI looks consistent (or better).
- No more "string parsing" in `panel.py`.
- Code is robust against text changes.
