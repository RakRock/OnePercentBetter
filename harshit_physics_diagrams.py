"""Backward-compatible shim. Prefer ``harshit.physics.diagrams``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.diagrams")
sys.modules[__name__] = _impl
