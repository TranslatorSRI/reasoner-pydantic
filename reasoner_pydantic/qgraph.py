"""Query graph models."""

from enum import Enum

from pydantic.class_validators import validator
from reasoner_pydantic.utils import HashableMapping
from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .utils import HashableMapping, HashableSequence, nonzero_validator
from .shared import BiolinkEntity, BiolinkPredicate, CURIE, KnowledgeType, Qualifier


class Operator(str, Enum):
    """Operator."""

    equal_to = "=="
    deep_equal_to = "==="
    greater_than = ">"
    less_than = "<"
    matches = "matches"


class AttributeConstraint(BaseModel):
    """QNode or QEdge attribute constraint."""

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


class QualifierConstraint(BaseModel):
    """QEdge Qualifier constraint."""

    qualifier_set: HashableSequence[Qualifier] = Field(
        default=HashableSequence[Qualifier](__root__=[]),
        title="qualifier set",
    )


class PathConstraint(BaseModel):
    """QPath Constraint."""

    intermediate_categories: Optional[HashableSequence[BiolinkEntity]]
    _nonzero_categories = validator("intermediate_categories", allow_reuse=True)(
        nonzero_validator
    )


class SetInterpretationEnum(str, Enum):
    """Enumeration for set interpretation."""

    BATCH = "BATCH"
    ALL = "ALL"
    MANY = "MANY"


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

    set_interpretation: Optional[SetInterpretationEnum] = Field("BATCH", nullable=True)

    constraints: Optional[HashableSequence[AttributeConstraint]] = Field(
        default=HashableSequence[AttributeConstraint](__root__=[]),
        title="attribute constraints",
    )

    member_ids: Optional[HashableSequence[CURIE]] = Field(
        default=HashableSequence[CURIE](__root__=[]), title="set member ids"
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

    knowledge_type: Optional[KnowledgeType] = Field(None, title="knowledge type")

    predicates: Optional[HashableSequence[BiolinkPredicate]] = Field(
        None,
        title="predicates",
        nullable=True,
    )
    _nonzero_predicates = validator("predicates", allow_reuse=True)(nonzero_validator)

    attribute_constraints: Optional[HashableSequence[AttributeConstraint]] = Field(
        default=HashableSequence[AttributeConstraint](__root__=[]),
        title="attribute constraints",
    )

    qualifier_constraints: Optional[HashableSequence[QualifierConstraint]] = Field(
        default=HashableSequence[QualifierConstraint](__root__=[]),
        title="qualifier constraint",
    )

    class Config:
        title = "query-graph edge"
        extra = "allow"
        allow_population_by_field_name = True


class QPath(BaseModel):
    """Query path."""

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

    constraints: Optional[HashableSequence[PathConstraint]]


class BaseQueryGraph(BaseModel):
    """Base query graph."""

    nodes: HashableMapping[str, QNode] = Field(
        ...,
        title="dict of nodes",
    )

    class Config:
        title = "Base query graph"
        extra = "allow"


class QueryGraph(BaseQueryGraph):
    """Traditional query graph."""

    edges: HashableMapping[str, QEdge] = Field(
        ...,
        title="dict of edges",
    )

    class Config:
        title = "simple query graph"
        extra = "allow"


class PathfinderQueryGraph(BaseQueryGraph):
    """Pathfinder query graph."""

    paths: HashableMapping[str, QPath] = Field(
        ...,
        title="dict of paths",
    )

    class Config:
        title = "pathfinder query graph"
        extra = "allow"
