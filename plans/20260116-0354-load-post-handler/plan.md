# Plan: Persistent Activation on File Load

## Context
User reports license does not auto-activate when opening external .blend files.
Goal: Re-trigger `auto_activate_license` after every file load event.

## 1. Implementation
- **File**: `__init__.py`.
- **Change**: 
    - Decorate a wrapper for `auto_activate_license` with `@persistent` (from `bpy.app.handlers`).
    - Register this wrapper to `bpy.app.handlers.load_post`.
    - Also ensure `auto_activate_license` is robust against being called multiple times (it already checks if thread is running, so it's safe).

## 2. Technical Details
- `run_activation_handler(dummy)`: Handler functions need to accept one argument (dummy).
- `@persistent`: Crucial. Without this, the handler is cleared when a new file loads (which defeats the purpose).

## 3. Risks
- **Infinite Loop?** No, `load_post` only fires when file loading finishes.
- **Race Condition**: File load -> Handler -> Async Thread. Safe.

## 4. Execution
- We will modify `__init__.py` to import `load_post` and register the handler.
