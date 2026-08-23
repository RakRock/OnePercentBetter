"""Backward-compatible shim. Prefer ``harshit.physics.components``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.components")
sys.modules[__name__] = _impl
