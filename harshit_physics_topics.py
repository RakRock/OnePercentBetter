"""Backward-compatible shim. Prefer ``harshit.physics.topics``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.topics")
sys.modules[__name__] = _impl
