from typing import Callable, Optional
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

    def __hash__(self) -> int:
        """Hash function based on Pydantic implementation"""
        return hash((self.__class__, tuple(self.__dict__.values())))

    def __eq__(self, other) -> bool:
        """Equality function that calls hash function"""
        return self.__hash__() == other.__hash__()

    def __setattr__(self, name, value):
        """Custom setattr that invalidates hash"""

        return super().__setattr__(name, value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.__custom_root_type__:
            return

    def update(self, other):
        """Update fields on this object with fields from other object"""
        raise NotImplementedError(
            f"Model {self.__class__.__name__} has no update method"
        )
