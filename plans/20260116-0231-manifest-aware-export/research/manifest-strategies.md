# Research Report: Manifest-Aware Export Strategy

## Topics Covered
1. **Standard Blender Manifest Patterns**: How `blender_manifest.toml` handles file exclusion.
2. **Alternative Manifest Strategies**: Using custom sections in TOML for specialized distribution.
3. **Implementation Tools**: Using `fnmatch` for pattern matching in Python export scripts.

## Insights
- **`paths_exclude_pattern`**: Blender 4.2+ natively supports this in `blender_manifest.toml`. It follows `.gitignore` style logic.
- **Custom Metadata**: We can add a non-standard section like `[sklum_export]` to store our internal "Production" vs "Develop" flag or specific include lists if `paths_exclude_pattern` isn't expressive enough.
- **`fnmatch` vs `pathlib.match`**: `fnmatch` is slightly more performant for simple string pattern matching during a walk, while `pathlib` offers cleaner syntax for complex path recursive checks.

## Recommendations
- **Primary**: Utilize the standard `paths_exclude_pattern` in `blender_manifest.toml`. This makes the addon compliant with Blender's official `extension build` tool as well.
- **Secondary**: Update the `/export` workflow to parse this TOML and apply the patterns dynamically.

## Unresolved Questions
- Should we allow the manifest to override global defaults (like `.git`) or should the script maintain a hard-coded "Sanity Blacklist"? (Recommendation: Hard-coded sanity list + user-defined manifest list).
