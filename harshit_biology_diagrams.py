"""Backward-compatible shim. Prefer ``harshit.biology.diagrams``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.diagrams")
sys.modules[__name__] = _impl
