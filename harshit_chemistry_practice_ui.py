"""Backward-compatible shim. Prefer ``harshit.chemistry.practice_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.practice_ui")
sys.modules[__name__] = _impl
