"""Backward-compatible shim. Prefer ``harshit.chemistry.ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.ui")
sys.modules[__name__] = _impl
