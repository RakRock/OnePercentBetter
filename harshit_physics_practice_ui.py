"""Backward-compatible shim. Prefer ``harshit.physics.practice_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.practice_ui")
sys.modules[__name__] = _impl
