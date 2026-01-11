# Blender API & Python Rules

- **Blender API Usage**:
    - Always use `context` (e.g., `context.active_object`) instead of `bpy.context` where available.
    - Avoid hardcoding object or material names.
    - Use `core.utils.safe_mode_set(mode)` when switching between Object and Edit modes.
    - Ensure all operators have a `poll` method to check for valid context before execution.
- **Structure**:
    - Keep operators and UI panels in separate files within their module folders.
    - Use the established `register()` and `unregister()` pattern in every module.
- **Error Handling**:
    - Wrap potential failure points in `try...except` blocks.
    - Use `core.utils.show_message_box` to report errors or important information to the user in the Blender UI.
- **Naming**:
    - Properties must be prefixed with `sklum_` to prevent namespace collisions with other addons.
    - Follow PEP 8 for Python code style.
- **Addon Packaging (QUAN TRỌNG)**:
    - Khi export addon, thư mục chứa addon **PHẢI** có tên trùng với tên module trong code (ví dụ: `SKLUMToolz`).
    - **KHÔNG BAO GIỜ** đặt tên thư mục có version (e.g., `SKLUMToolz_v2.5.5`) vì Blender sử dụng tên thư mục làm tên module Python.
    - Version chỉ được đặt trong tên file ZIP (e.g., `SKLUMToolz_v2.5.5.zip`), KHÔNG trong tên thư mục bên trong.

