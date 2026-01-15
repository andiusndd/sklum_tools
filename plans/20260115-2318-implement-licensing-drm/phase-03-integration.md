# Phase 3: Integration & Obfuscation

## Context
With Client and Server ready, we need to secure the Client code so users cannot easily remove the check.

## Implementation Steps
1.  **Connect Client to Real Server**:
    -   Update `core/license.py` to use the real Vercel URL.
2.  **Obfuscation with PyArmor**:
    -   Add a step in `/export` workflow to run `pyarmor gen`.
    -   Pack the `core/` folder (or at least `license.py`).
    -   Replace the clear text files with obfuscated files in the ZIP.
3.  **Final Test**:
    -   Verify the exported ZIP allows activation on Machine A.
    -   Verify it FAILS on Machine B (simulated by changing HWID mock).

## Todo List
- [x] Update `_export_addon.py` to support PyArmor.
- [x] Document the "Reset License" process for the admin.
