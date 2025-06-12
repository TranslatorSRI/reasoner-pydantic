import json
from typing import Any, Final, Generic, TypeVar

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
        return hash(
            (
                self.__class__.__name__,
                *(
                    (k, hash(v))
                    for k, v in {
                        **self.__dict__,
                        **(self.__pydantic_extra__ or {}),
                    }.items()
                ),
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

    # After running validation on all known properties, make sure everything else is hashable
    @model_validator(mode="before")
    @classmethod
    def make_hashable_root(cls, values: Any):
        # The root validator must take and return a dict
        return make_hashable(values)

    def to_dict(self) -> dict[Any, Any]:
        return json.loads(self.json())


RootType = TypeVar("RootType")


class RootModel(BaseModel, PydanticRootModel[RootType], Generic[RootType]):
    """
    Custom root model for all classes.

    This provides hash and equality methods.
    """
