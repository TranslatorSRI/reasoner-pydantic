from typing import Callable, Optional
import weakref
from pydantic import BaseModel as PydanticBaseModel, PrivateAttr


class BaseModel(PydanticBaseModel):
    """
    Custom base model for all classes

    This provides hash and equality methods.
    """

    def __hash__(self) -> int:
        """Hash function based on Pydantic implementation"""
        return hash((self.__class__, tuple(self.__dict__.values())))

    def __eq__(self, other) -> bool:
        """Equality function that calls hash function"""
        return self.__hash__() == other.__hash__()

    def update(self, other):
        """Update fields on this object with fields from other object"""
        raise NotImplementedError(
            f"Model {self.__class__.__name__} has no update method"
        )
