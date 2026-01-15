# Research Report: Blender Addon Modular Registration Best Practices

## Topics Covered
1. **Module Separation**: Standardizing `operators.py`, `panels.py`, `properties.py`.
2. **Import Management**: Preventing circular imports via relative imports and scoped imports.
3. **Registration Order**: Ensuring dependencies (properties) are registered before users (operators).
4. **Lazy Loading**: Optimizing startup time.

## Insights
- **Properties First**: PropertyGroups must be registered/attached to `bpy.types.Scene` before they are referenced in UI or Operators.
- **Top-Level Imports**: Avoid `from . import properties` at the top of submodules if `properties` also imports that submodule. Use `import importlib` and reload logic.
- **Unregister Order**: Always unregister in `reversed()` order of registration to prevent dependency orphans.

## Recommendations
- Implement a centralized `register()` in `__init__.py` that imports submodules *inside* the function.
- Use a `modules` list to maintain strict order.
- Define a boilerplate for `__init__.py` across all folders.

## Unresolved Questions
- None.
