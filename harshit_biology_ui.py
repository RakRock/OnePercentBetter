"""Backward-compatible shim. Prefer ``harshit.biology.ui``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.ui")
sys.modules[__name__] = _impl
