"""Backward-compatible shim. Prefer ``harshit.biology.topics``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.topics")
sys.modules[__name__] = _impl
