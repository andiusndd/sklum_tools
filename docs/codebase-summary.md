# Codebase Summary

## Directory Structure

```
SKLUMToolz/
├── __init__.py                # Main Entry Point
├── blender_manifest.toml      # Blender 4.2+ Extension Manifest
├── core/                      # Shared Logic & Utilities
│   ├── checker_logic.py       # Core algorithms for Mesh/UV checks
│   ├── license_logic.py       # DRM: HWID fetch & API validation
│   ├── utils.py               # Helper functions
│   ├── preferences.py         # Addon Preferences UI
│   └── ...
├── panel_checker_tools/       # [PANEL] QA Tools
│   ├── check_all/             # "Check All" Orchestrator
│   ├── license_manager/       # DRM UI & Operators
│   └── ...
├── panel_import_export/       # [PANEL] IO Automation
├── panel_jpg_converter/       # [PANEL] Image Processing
├── panel_auto_rename/         # [PANEL] Batch Renaming
├── panel_object_setting/      # [PANEL] General Object Tools
├── server_backend/            # [EXTERNAL] Server-side Code
│   ├── api/index.py           # Vercel Serverless Function
│   └── schema.sql             # Supabase Database Schema
└── docs/                      # Project Documentation
```

## Module Responsibilities

### Core Modules
- **`core.checker_logic`**: Pure Python functions (mostly) that take Blender objects and return validation results (Pass/Fail). Decoupled from UI code where possible.
- **`core.license_logic`**: Handles the critical security loop.
    - `get_machine_id`: Uses `wmic` on Windows to get unique motherboard UUID.
    - `validate_license`: HTTPS call to Vercel API.

### UI Panels (`panel_*`)
Each panel follows a modular structure:
- `panel.py`: Defines `bpy.types.Panel` classes for drawing the UI.
- `operator.py`: Defines `bpy.types.Operator` for action logic.
- `properties.py`: Defines `bpy.types.PropertyGroup` for UI state.
- `__init__.py`: Registry for the module.

### Backend (`server_backend`)
*Not distributed with the Addon Zip.*
- **Technology**: Python Http.server (Vercel Adapter).
- **Database**: PostgreSQL (Supabase) storing `licenses` table.

## Key Data Stuctures
- **`CheckResult`** (`core/checker_logic.py`): Standardized DTO for validation results (Status, Message, Failed Objects List).
- **`SKLUM_CheckResultItem`** (`panel_checker_tools/properties.py`): Blender CollectionProperty items for displaying results in a structured UI list.
- **License Data**: Stored in `Scene.sklum_license_key` (Transient) or Addon Preferences (Persistent - *Planned*).
