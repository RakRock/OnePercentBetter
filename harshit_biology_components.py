"""Backward-compatible shim. Prefer ``harshit.biology.components``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.components")
sys.modules[__name__] = _impl
