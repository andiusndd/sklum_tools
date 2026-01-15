# Phase 01: Manifest Definition

## Context
- **Reference Plan:** [plan.md](./plan.md)
- **Goal:** Centralize exclusion rules in the official Blender manifest.

## Overview
- **Date:** 2026-01-16
- **Description:** Implement `paths_exclude_pattern` in TOML.
- **Priority:** HIGH
- **Implementation Status:** PENDING

## Requirements
- Must include all current dev folders: `.git`, `.agent`, `.gemini`, `docs`, `plans`, `tests`, `server_backend`, `logs`, `__pycache__`.
- Must exclude temporary `.zip` files and the export script itself.

## Related code files
- `blender_manifest.toml`

## Implementation Steps
1. **Modify `blender_manifest.toml`**: Add the `paths_exclude_pattern` array with glob patterns.
2. **Verify TOML Integrity**: Use `tomllib` (via a quick python one-liner) to ensure the file is still valid.

## Success Criteria
- The manifest file contains accurate exclusion patterns.
