"""Backward-compatible shim. Prefer ``harshit.chemistry.mcq_ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.mcq_ui")
sys.modules[__name__] = _impl
