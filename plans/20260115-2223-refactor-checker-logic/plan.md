# Refactor Checker Logic

## Overview
- **Goal**: Refactor the brittle string-based check logic into a robust, object-oriented architecture.
- **Status**: Planning
- **Priority**: High (Technical Debt)

## Implementation Phases

### [Phase 1: Core Logic Refactor](./phase-01-core-refactor.md)
- **Status**: Pending
- **Description**: create `core/checker_logic.py` and migrate check logic from operators to pure functions returning structured data.

### [Phase 2: UI & Property Integration](./phase-02-ui-integration.md)
- **Status**: Pending
- **Description**: Update `properties.py` to use CollectionProperty for results and update `panel.py` to render them.

## Success Criteria
- No more string matching (`if "LỖI" in result`).
- Logic is centralized in `core/`.
- UI displays results from structured data.
