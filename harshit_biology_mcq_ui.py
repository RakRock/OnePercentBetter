"""Backward-compatible shim. Prefer ``harshit.biology.mcq_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.mcq_ui")
sys.modules[__name__] = _impl
