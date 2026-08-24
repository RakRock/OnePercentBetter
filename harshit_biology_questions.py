"""Backward-compatible shim. Prefer ``harshit.biology.questions``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.questions")
sys.modules[__name__] = _impl
