# Code Standards & Structure: SKLUM Tools

## 1. Modular Registration
All sub-packages must implement `register()` and `unregister()` functions.
- **Lazy Loading**: Import sub-modules *inside* the `register()` function using `importlib.import_module` to prevent circular dependencies.
- **Safe Loops**: Use `try-except` blocks when iterating through sub-modules to register them.
- **Reversed Unregistration**: Always call `reversed(sub_packages)` during unregistration.

## 2. Naming Conventions
- **Internal Variables**: Use snake_case (e.g., `license_active`).
- **Blender Ops**: Use `SKLUM_OT_name_of_op`.
- **Blender Panels**: Use `VIEW3D_PT_sklum_name`.
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `REPO_URL`).

## 3. Logging & Error Handling
- **No loose `print()`**: Use `core.logger.logger.info()` or `logger.error()`.
- **Defensive FS Ops**: Use `core.utils.safe_remove` for file deletions on Windows.
- **User Feedback**: Errors in operators should use `self.report({'ERROR'}, msg)` in addition to logging.

## 4. UI Consistency
- All panels should be under the `SKLUM Tools` tab in the Sidebar.
- Use `layout.box()` for distinct tool groups.
- Display status icons next to check results (✅ / ⚠️).
