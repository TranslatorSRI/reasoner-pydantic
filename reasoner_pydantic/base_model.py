import json

from pydantic import BaseModel as PydanticBaseModel

from pydantic.class_validators import root_validator
from .utils import make_hashable


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

    # After running validation on all known properties, make sure everything else is hashable
    @root_validator(allow_reuse=True, pre=False)
    def make_hashable_root(cls, values):
        # The root validator must take and return a dict
        return {k: make_hashable(v) for k, v in values.items()}

    def to_dict(self) -> dict:
        return json.loads(self.json())
