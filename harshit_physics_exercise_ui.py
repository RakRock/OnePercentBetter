"""Backward-compatible shim. Prefer ``harshit.physics.exercise_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.exercise_ui")
sys.modules[__name__] = _impl
