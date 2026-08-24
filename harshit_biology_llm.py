"""Backward-compatible shim. Prefer ``harshit.biology.llm``."""
import importlib
import sys

_impl = importlib.import_module("harshit.biology.llm")
sys.modules[__name__] = _impl
