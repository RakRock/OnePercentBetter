"""Backward-compatible shim. Prefer ``harshit.chemistry.components``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.components")
sys.modules[__name__] = _impl
