"""Backward-compatible shim. Prefer ``harshit.chemistry.diagrams``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.diagrams")
sys.modules[__name__] = _impl
