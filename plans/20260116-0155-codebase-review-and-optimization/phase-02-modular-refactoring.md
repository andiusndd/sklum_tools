# Phase 2: Modular Refactoring

## Overview
Cleaning up the registration logic to prevent "partially initialized module" errors and ensure clean unregistration.

## Implementation Steps
1.  **Strict Registration Order**: Maintain the sequence: `core` -> `panels`.
2.  **Explicit Unregister**: Ensure `reversed(modules)` is used for cleanup.
3.  **Lazy Imports**: Move some heavy imports inside `register()` if they cause startup lag.
