"""Backward-compatible shim. Prefer ``harshit.biology.state``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.state")
sys.modules[__name__] = _impl
