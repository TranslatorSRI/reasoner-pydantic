from pydantic import BaseModel as PydanticBaseModel

from pydantic.class_validators import root_validator
from .utils import HashableMapping, HashableSequence, make_hashable

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

    def make_hashable(cls, values):
        """
        Convert a generic Python object to a hashable one recursively

        This is an expensive operation, so it is best used sparingly
        """

        # type(o) is faster than isinstance(o) because it doesn't
        # traverse the inheritance hierarchy
        o_type = str(type(values))
        
        new_value = values
        if "dict" in o_type:
            new_value = HashableMapping.parse_obj(((k, cls.make_hashable(v)) for k, v in values.items()))
        if "list" in o_type:
            new_value = HashableSequence.parse_obj(cls.make_hashable(v) for v in values)

        return new_value

    @root_validator(allow_reuse=True, pre=False)
    def make_hashable_root(cls, values):
        # The root validator must take and return a dict
        return {k: make_hashable(k) for k, v in values.items()}

