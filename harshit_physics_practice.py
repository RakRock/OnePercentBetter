"""Backward-compatible shim. Prefer ``harshit.physics.practice``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.practice")
sys.modules[__name__] = _impl
