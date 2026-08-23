"""Backward-compatible shim. Prefer ``harshit.chemistry.llm``."""
import importlib
import sys

_impl = importlib.import_module("harshit.chemistry.llm")
sys.modules[__name__] = _impl
