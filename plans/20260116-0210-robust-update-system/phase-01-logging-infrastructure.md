# Phase 01: Centralized Logging Infrastructure

## Context
- **Reference Plan:** [plan.md](./plan.md)
- **Goal:** Replace scattered `print()` statements with a structured logging system.

## Overview
- **Date:** 2026-01-16
- **Implementation Status:** PENDING
- **Priority:** MEDIUM

## Key Insights
- Standard `logging` module is preferred for extensibility.
- Log file should be located in a dedicated `logs` folder within the addon or in the system temp dir (better for Windows permissions).

## Requirements
- Support `DEBUG`, `INFO`, `WARNING`, `ERROR` levels.
- Concurrent logging to System Console and a File.
- Automatic log folder creation.

## Architecture
```python
# core/logger.py
import logging
import os

logger = logging.getLogger("SKLUM")
# ... handlers setup ...
```

## Related code files
- `core/logger.py` (New)
- `__init__.py` (For initialization)

## Implementation Steps
1. Create `core/logger.py`.
2. Configure `SKLUM` logger with `FileHandler` and `StreamHandler`.
3. Update `__init__.py` to call `logger.init()` on register.
4. Replace existing `print("[SKLUM] ...")` with `logger.info(...)`.

## Success Criteria
- A `sklum_tools.log` file is created on startup.
- Logs appear in both the console and the file.
