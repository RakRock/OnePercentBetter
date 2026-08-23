"""Backward-compatible shim. Prefer ``harshit.chemistry.questions``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.questions")
sys.modules[__name__] = _impl
