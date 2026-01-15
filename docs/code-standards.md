# Code Standards & Guidelines

## 1. Naming Conventions

### Blender Entities
To avoid collisions with other addons, all Global properties and Classes MUST use the `SKLUM` prefix (or `sklum` for variables).

- **Operators**: `SKLUM_OT_action_name` (e.g., `SKLUM_OT_check_all`)
    - `bl_idname`: `"sklum.action_name"`
- **Panels**: `VIEW3D_PT_sklum_panel_name`
- **Properties (Scene/Object)**: `sklum_property_name` (e.g., `bpy.types.Scene.sklum_license_key`)
- **UI Lists**: `SKLUM_UL_list_name`

### Python Code
- **Variables/Functions**: `snake_case` (e.g., `check_uv_map`)
- **Classes**: `CamelCase` (e.g., `CheckResult`)
- **Constants**: `UPPER_CASE` (e.g., `DEFAULT_ANGLE`)

## 2. Directory Structure
- **Modularity**: New features should be encapsulated in their own `panel_feature_name` directory.
- **Registration**:
    - Each module must have `register()` and `unregister()`.
    - `__init__.py` in the root aggregates these calls.
    - Avoid direct `bpy.utils.register_class` in the root `__init__.py`.

## 3. UI Guidelines (Aesthetics)
- **Colors**:
    - Use `layout.alert = True` (Red) for Errors/Failures.
    - Use standard Grey/Theme colors for Information.
    - DO NOT use `layout.alert = False` explicitly to force Green (Blender doesn't support Green alerts natively without tricks), rely on Icons instead.
- **Icons**:
    - Pass: `CHECKMARK`
    - Fail: `ERROR`
    - Info: `INFO`
    - Action: Relevant action icon (e.g., `FILE_REFRESH`).
- **Layout**:
    - Use `layout.box()` to group related controls.
    - Use headers with Collapse/Expand arrows for complex sections.

## 4. Error Handling
- **Graceful Failure**: Operators should return `{'CANCELLED'}` on failure, not crash.
- **Reporting**: Use `self.report({'ERROR'}, "Message")` to notify users.
- **DRM**: License checks should fail silently or clearly (no crashes) when internet is down.

## 5. Security (DRM)
- **Sensitive Logic**: Code in `core/license_logic.py` is sensitive.
- **Obfuscation**: This file must be obfuscated via PyArmor during the `/export` workflow.
- **Hardcoding**: Do NOT hardcode License Keys in client code.
