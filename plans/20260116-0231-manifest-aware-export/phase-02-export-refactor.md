# Phase 02: Export Engine Refactor

## Context
- **Reference Plan:** [plan.md](./plan.md)
- **Goal:** Update the workspace automation to respect the manifest.

## Overview
- **Date:** 2026-01-16
- **Description:** Implement the new copy logic in the `/export` workflow.
- **Priority:** HIGH
- **Implementation Status:** PENDING

## Requirements
- Use `tomllib` to load `paths_exclude_pattern`.
- Implement `fnmatch` to filter files/folders during the `os.walk`.
- Ensure root-level files like `README.md` and `LICENSE` are still included unless explicitly excluded.

## Implementation Steps
1. **Update `export.md` Python Script**:
    - Add logic to load `blender_manifest.toml`.
    - Replace the hard-coded `top_level` check with a pattern-matching loop.
    - Simplified logic: if a path matches *any* pattern in the exclude list, skip it.
2. **Handle Special Files**: Ensure `blender_manifest.toml` itself is always included.

## Success Criteria
- Running `/export` produces a `.zip` that has exactly what the manifest permits.
- Adding a new folder like `resources/` results in it being included automatically (since it's not in the exclude list).
