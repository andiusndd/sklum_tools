# Blender API Rules

## Deprecated/Removed Icons (Blender 4.0+)
- `WIRE` -> Use `SHADING_WIRE`
- `BOUNDS` -> Use `SHADING_BBOX`
- `ORIENTATION_EXTERNAL` -> Removed
- `PARENT_DEFORMED` -> Removed

## UI & Layout
- `UILayout.split()`: Use `align=True` for cleaner layouts.
- `UILayout.prop(toggle=True)`: Use for boolean properties to simulate buttons.

## Release & Versioning (Blender 4.2 Extensions)
- Always use `blender_manifest.toml` as the source of truth.
- `bl_info` in `__init__.py` is deprecated but kept for backward compatibility (optional).
