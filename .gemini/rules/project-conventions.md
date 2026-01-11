# Project Conventions & Documentation

- **Documentation Documentation**:
    - Update `STRUCTURE.md` immediately if the project hierarchy changes.
    - Record every significant change or bug fix in `UPDATE-LOG.md` under the current version.
    - Maintain `README.md` as the primary source of truth for features and installation.
- **Code Organization**:
    - Place generic helper functions in `core/utils.py`.
    - Define all shared constants (tolerances, naming keywords) in `core/constants.py`.
    - New feature sets should be placed in a new `panel_*` directory.
- **Refactoring**:
    - When refactoring, maintain backward compatibility within the `major.minor` version if possible.
    - Follow the "modular registration" pattern defined in `STRUCTURE.md`.
