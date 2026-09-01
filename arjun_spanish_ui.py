"""Backward-compatible shim. Prefer ``arjun_spanish.ui``."""
import importlib
import sys

_impl = importlib.import_module("arjun_spanish.ui")
sys.modules[__name__] = _impl
