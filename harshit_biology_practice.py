"""Backward-compatible shim. Prefer ``harshit.biology.practice``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.practice")
sys.modules[__name__] = _impl
