"""Query graph models."""
from enum import Enum

from pydantic.class_validators import validator
from reasoner_pydantic.utils import HashableMapping
from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .utils import HashableMapping, HashableSequence, nonzero_validator
from .shared import BiolinkEntity, BiolinkPredicate, CURIE


class Operator(str, Enum):
    """Operator."""

    equal_to = "=="
    greater_than = ">"
    less_than = "<"
    matches = "matches"


class QueryConstraint(BaseModel):
    """QNode or QEdge constraint."""

    name: str = Field(
        ...,
        title="name",
        nullable=False,
    )
    id: CURIE = Field(
        ...,
        title="id",
        nullable=False,
    )
    negated: bool = Field(
        False,
        title="not",
        alias="not",
    )
    operator: Operator = Field(
        ...,
        title="operator",
    )
    value: Any = Field(
        ...,
        title="value",
    )
    unit_id: Optional[Any] = Field(
        None,
        title="unit_id",
    )
    unit_name: Optional[Any] = Field(
        None,
        title="unit_name",
    )

    class Config:
        extra = "forbid"

    def dict(self, *args, **kwargs):
        output = super().dict(*args, **kwargs)
        output["not"] = output.pop("negated", False)
        return output


class QNode(BaseModel):
    """Query node."""

    ids: Optional[HashableSequence[CURIE]] = Field(
        None,
        title="ids",
        nullable=True,
    )
    _nonzero_ids = validator("ids", allow_reuse=True)(nonzero_validator)

    categories: Optional[HashableSequence[BiolinkEntity]] = Field(
        None,
        title="categories",
        nullable=True,
    )
    _nonzero_categories = validator("categories", allow_reuse=True)(nonzero_validator)

    is_set: bool = False
    constraints: Optional[HashableSequence[QueryConstraint]] = Field(
        default=HashableSequence[QueryConstraint](__root__=[]),
        title="constraints",
    )

    class Config:
        title = "query-graph node"
        extra = "allow"
        allow_population_by_field_name = True


class QEdge(BaseModel):
    """Query edge."""

    subject: str = Field(
        ...,
        title="subject node id",
    )
    object: str = Field(
        ...,
        title="object node id",
    )

    predicates: Optional[HashableSequence[BiolinkPredicate]] = Field(
        None,
        title="predicates",
        nullable=True,
    )
    _nonzero_predicates = validator("predicates", allow_reuse=True)(nonzero_validator)

    constraints: Optional[HashableSequence[QueryConstraint]] = Field(
        default=HashableSequence[QueryConstraint](__root__=[]),
        title="constraints",
    )

    class Config:
        title = "query-graph edge"
        extra = "allow"
        allow_population_by_field_name = True


class QueryGraph(BaseModel):
    """Query graph."""

    nodes: HashableMapping[str, QNode] = Field(
        ...,
        title="dict of nodes",
    )
    edges: HashableMapping[str, QEdge] = Field(
        ...,
        title="dict of edges",
    )

    class Config:
        title = "simple query graph"
        extra = "allow"
