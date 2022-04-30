"""Results models."""
from typing import Optional, Any

from pydantic import Field
from pydantic.class_validators import validator, root_validator

from .base_model import BaseModel
from .utils import HashableMapping, HashableSequence, HashableSet
from .shared import Attribute, CURIE


class EdgeBinding(BaseModel):
    """Edge binding."""

    id: str = Field(
        ...,
        title="knowledge graph id",
    )

    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "edge binding"
        schema_extra = {
            "example": {
                "id": "string",
            },
        }
        extra = "allow"


class NodeBinding(BaseModel):
    """Node binding."""

    id: CURIE = Field(
        ...,
        title="knowledge graph id",
    )

    class Config:
        title = "node binding"
        schema_extra = {
            "example": {
                "id": "x:string",
            },
        }
        extra = "allow"


class Result(BaseModel):
    """Result."""

    node_bindings: HashableMapping[str, HashableSet[NodeBinding]] = Field(
        ...,
        title="list of node bindings",
    )
    edge_bindings: HashableMapping[str, HashableSet[EdgeBinding]] = Field(
        ...,
        title="list of edge bindings",
    )
    score: Optional[float] = Field(
        None,
        format="float",
    )
    # these lines work
    # raw_data: Optional[Any] = Field(
    #     None
    # )
    # _make_fields_hashable = validator("*", allow_reuse=True, check_fields=False)(make_hashable)

    # this isn't working
    @root_validator(pre=True, allow_reuse=True)
    def make_hashable(cls, values):
        """
        Convert a generic Python object to a hashable one recursively

        This is an expensive operation, so it is best used sparingly
        """

        # type(o) is faster than isinstance(o) because it doesn't
        # traverse the inheritance hierarchy
        o_type = str(type(values))
        print(o_type)
        print(values)

        if "dict" in o_type:
            print('got a dict')
            return HashableMapping.parse_obj(((k, cls.make_hashable(cls, v)) for k, v in values.items()))
        if "list" in o_type:
            print('got a list')
            return HashableSequence.parse_obj(cls.make_hashable(cls, v) for v in values)

        return values

    class Config:
        title = "result"
        extra = "allow"
