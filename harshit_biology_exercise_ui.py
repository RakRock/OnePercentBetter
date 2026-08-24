"""Backward-compatible shim. Prefer ``harshit.biology.exercise_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.exercise_ui")
sys.modules[__name__] = _impl
