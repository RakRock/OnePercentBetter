"""Backward-compatible shim. Prefer ``harshit.physics.content``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.content")
sys.modules[__name__] = _impl
