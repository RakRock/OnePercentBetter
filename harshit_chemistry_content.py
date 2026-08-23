"""Backward-compatible shim. Prefer ``harshit.chemistry.content``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.content")
sys.modules[__name__] = _impl
