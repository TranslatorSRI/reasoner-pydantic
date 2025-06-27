import json
from typing import Any, Final, Generic, Self, TypeVar

from pydantic import (
    model_validator,
    BaseModel as PydanticBaseModel,
    RootModel as PydanticRootModel,
)

from .utils import make_hashable


class BaseModel(PydanticBaseModel):
    """
    Custom base model for all classes

    This provides hash and equality methods.
    """

    def __hash__(self) -> int:
        """Hash function based on Pydantic implementation"""
        # Faster than calling tuple() or otherwise unpacking dictionaries
        return hash(
            (
                self.__class__.__name__,
                *self.__dict__.items(),
                *((self.model_extra or {}).items()),
            )
        )

    def __eq__(self, other: object) -> bool:
        """Equality function that calls hash function"""
        return self.__hash__() == other.__hash__()

    def update(self, _other: object) -> None:
        """Update fields on this object with fields from other object"""
        raise NotImplementedError(
            f"Model {self.__class__.__name__} has no update method"
        )

    def get_field(self, field: str):
        return getattr(self, field, None)

    @model_validator(mode="after")
    def ensure_hashable_extra(self) -> Self:
        """Ensure extra fields are hashable, if they're allowed."""
        if not self.model_extra:
            return self
        for k, v in self.model_extra.items():
            self.model_extra[k] = make_hashable(v)
        return self

    def to_dict(self) -> dict[Any, Any]:
        """DEPRECATED: use model_dump() instead."""
        return self.model_dump()


RootType = TypeVar("RootType")


class RootModel(BaseModel, PydanticRootModel[RootType], Generic[RootType]):
    """
    Custom root model for all classes.

    This provides hash and equality methods.
    """
