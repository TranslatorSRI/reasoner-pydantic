from typing import Callable
import weakref
from pydantic import BaseModel as PydanticBaseModel, PrivateAttr


class BaseModel(PydanticBaseModel):
    """
    Custom base model for all classes

    This provides a hash function that assumes all fields are either:

    1. Immutable
    2. Derived from BaseModel
    3. Able to call a hash invalidation hook on their own
    """

    _hash: int = PrivateAttr(default=None)
    _invalidate_hook: Callable = PrivateAttr(default=None)

    def __hash__(self) -> int:
        """Hash function based on Pydantic implementation"""
        if not self._hash:
            self._hash = hash((self.__class__, tuple(self.__dict__.values())))
        return self._hash

    def __eq__(self, other) -> bool:
        """Equality function that calls hash function"""
        return self.__hash__() == other.__hash__()

    def __setattr__(self, name, value):
        """Custom setattr that invalidates hash"""

        if name != "_hash":
            self.invalidate_hash()
        return super().__setattr__(name, value)

    def invalidate_hash(self):
        """Invalidate stored hash value"""
        self._hash = None
        # Propogate
        if self._invalidate_hook:
            self._invalidate_hook()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.__custom_root_type__:
            return

        # Look for BaseModel fields and give them a hook
        # that they can use to invalidate hash on this object
        for value in self.__dict__.values():
            if hasattr(value, "_invalidate_hook"):
                value._invalidate_hook = self.invalidate_hash

    def update(self, other):
        """Update fields on this object with fields from other object"""
        raise NotImplementedError(
            f"Model {self.__class__.__name__} has no update method"
        )

    class Config:
        validate_assignment = True
