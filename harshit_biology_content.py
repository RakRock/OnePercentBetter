"""Backward-compatible shim. Prefer ``harshit.biology.content``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.content")
sys.modules[__name__] = _impl
