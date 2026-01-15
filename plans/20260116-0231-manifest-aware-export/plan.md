# Plan: Manifest-Aware Export System

## Overview
Transform the `/export` workflow from a hard-coded whitelist approach to a dynamic, manifest-driven system. This ensures that new features (folders) are automatically included unless explicitly excluded in `blender_manifest.toml`.

## Status
- **Phase 1: Manifest Definition**: Completed
- **Phase 2: Export Engine Refactor**: Completed

## Progress
- Total Progress: 0%

## Phases

### [Phase 1: Manifest Definition](./phase-01-manifest-definition.md)
Update `blender_manifest.toml` with `paths_exclude_pattern` containing all development-only folders.

### [Phase 2: Export Engine Refactor](./phase-02-export-refactor.md)
Update `.agent/workflows/export.md` to use the manifest for exclusion logic, making the copy process "Negative-only".
