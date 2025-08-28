"""
mnt/data/src/data/models/__init__.py
====================================

This module serves as the package initializer for all data model classes.
It exposes model classes for easy imports and supports future extensions.

Example usage:
    from data.models import UserModel, TransactionModel
"""

from typing import TYPE_CHECKING

# Conditional imports for type hints (avoids circular imports at runtime)
if TYPE_CHECKING:
    from .user_model import UserModel
    from .transaction_model import TransactionModel

# Explicitly define public API of this package
__all__ = [
    "UserModel",
    "TransactionModel",
]

# Optional lazy import to avoid loading all models immediately
import importlib

class _LazyLoader:
    def __init__(self, name_map):
        self._name_map = name_map

    def __getattr__(self, item):
        if item in self._name_map:
            module_name, class_name = self._name_map[item]
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            setattr(self, item, cls)
            return cls
        raise AttributeError(f"Module '{__name__}' has no attribute '{item}'")

# Map of class names to their module paths
_lazy_models = {
    "UserModel": ("mnt.data.src.data.models.user_model", "UserModel"),
    "TransactionModel": ("mnt.data.src.data.models.transaction_model", "TransactionModel"),
}

# Replace current module with lazy loader
import sys
sys.modules[__name__] = _LazyLoader(_lazy_models)
