"""Backward-compatible shim. Prefer ``harshit.biology.practice_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.practice_ui")
sys.modules[__name__] = _impl
