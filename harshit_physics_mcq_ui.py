"""Backward-compatible shim. Prefer ``harshit.physics.mcq_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.mcq_ui")
sys.modules[__name__] = _impl
