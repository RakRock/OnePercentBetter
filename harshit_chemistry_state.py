"""Backward-compatible shim. Prefer ``harshit.chemistry.state``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.state")
sys.modules[__name__] = _impl
