# Research Report: Performance & UX Optimization in Blender

## Topics Covered
1. **Asynchronous API Calls**: How to avoid blocking the UI thread during network validation.
2. **Persistence & Caching**: Best practices for storing session-based or periodic validation status.
3. **Optimizing Computational Checks**: Using generators or modal operators for batch processing.

## Insights
- **Async Threading**: `threading.Thread` can be used for the network request. To update Blender's internal state safely, a `bpy.app.timers` check or a modal operator should poll a "result" variable.
- **Persistent Validation**: Storing a "checked_at" timestamp in `AddonPreferences` allows the addon to skip the network hit on every load. A 24-48 hour TTL (Time To Live) is recommended for security.
- **HWID Speed**: `subprocess` calls take 100-300ms. Caching this in a global variable after the first call makes subsequent checks near-instant.
- **Progress Bars**: `window_manager.progress_begin(min, max)` and `progress_update(value)` are the standard way to show simple progress in the status bar/cursor.

## Recommendations
- Implement a `ThreadedValidator` in `core/license_logic.py`.
- Add a `last_validated` `FloatProperty` in `SKLUM_SceneSettings` or `AddonPreferences`.
- Add a tiny "refresh" pulse or icon to the UI when background checks are happening.

## Unresolved Questions
- Should we provide an "Offline Mode"? (Recommendation: No, given the DRM requirement).
