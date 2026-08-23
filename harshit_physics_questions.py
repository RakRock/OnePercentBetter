"""Backward-compatible shim. Prefer ``harshit.physics.questions``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.questions")
sys.modules[__name__] = _impl
