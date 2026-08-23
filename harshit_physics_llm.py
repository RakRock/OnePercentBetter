"""Backward-compatible shim. Prefer ``harshit.physics.llm``."""
import importlib
import sys

_impl = importlib.import_module("harshit.physics.llm")
sys.modules[__name__] = _impl
