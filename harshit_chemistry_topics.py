"""Backward-compatible shim. Prefer ``harshit.chemistry.topics``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.topics")
sys.modules[__name__] = _impl
