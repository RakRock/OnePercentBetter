"""Backward-compatible shim. Prefer ``harshit.physics.ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.ui")
sys.modules[__name__] = _impl
