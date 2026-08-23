"""Backward-compatible shim. Prefer ``harshit.physics.state``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.state")
sys.modules[__name__] = _impl
