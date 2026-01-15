# Scout Report: Current Export Vulnerabilities

## Observed Logic
In `.agent/workflows/export.md`:
```python
EXCLUDE_DIRS = {'docs', 'plans', 'tests', 'server_backend', 'logs', '.agent', '.gemini', '.git'}
# ...
if not (top_level == "core" or top_level.startswith("panel_") or top_level == "docs"):
    continue
```

## Issues Identified
- **Stale Whitelist**: If a developer adds an `assets/` folder, the current script will skip it because it doesn't start with `panel_`.
- **Manual Sync**: Every time a new "Infrastructure" folder (docs, plans, local_db) is added, the script must be manually updated.
- **Legacy Logic**: The current script still has `if top_level == "docs": continue` which contradicts the intent to keep it clean.

## Actionable Targets
- [ ] Move the exclusion list to `blender_manifest.toml` under `paths_exclude_pattern`.
- [ ] Refactor `/export` to be "Negative-only": Exclude what is listed, Include everything else.
- [ ] Use `tomllib` to read the manifest directly in the export script.
