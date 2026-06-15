# app.modules.batches is imported as a Python package by app/main.py through
# app/modules/batches/router.py.
#
# CONVENTION — why this file stays empty
# ----------------------------------------
# Python requires an __init__.py for a directory to be a package. Beyond that
# requirement this file intentionally contains no imports or side-effects.
#
# Putting imports here (e.g. `from .router import router`) would execute them
# the moment any part of the application imports the *package*, not just the
# specific sub-module it needs. That can cause:
#   - Circular import errors during startup if two modules import each other.
#   - Unexpected database or filesystem access during test collection.
#   - Slower cold-start times because all module code is loaded eagerly.
#
# Instead, every consumer imports exactly what it needs directly:
#   from app.modules.batches.router import router
#   from app.modules.batches.service import BatchService
