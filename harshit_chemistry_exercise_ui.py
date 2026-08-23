"""Backward-compatible shim. Prefer ``harshit.chemistry.exercise_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.exercise_ui")
sys.modules[__name__] = _impl
