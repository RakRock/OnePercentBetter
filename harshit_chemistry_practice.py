"""Backward-compatible shim. Prefer ``harshit.chemistry.practice``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.practice")
sys.modules[__name__] = _impl
