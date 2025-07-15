"""Query graph models."""

from enum import Enum

from typing import Annotated, Any, Optional

from pydantic import AfterValidator, ConfigDict, Field, model_serializer

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

    name: str
    id: CURIE
    negated: Annotated[
        bool,
        Field(
            False,
            title="not",
            alias="not",
        ),
    ]
    operator: Operator
    value: Any
    unit_id: Optional[Any] = None
    unit_name: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")

    @model_serializer
    def serialize(self):
        """Replace `negated` with `not`."""
        output = self.__dict__
        output["not"] = output.pop("negated", False)
        return output


class QualifierConstraint(BaseModel):
    """QEdge Qualifier constraint."""

    qualifier_set: HashableSequence[Qualifier] = Field(
        title="qualifier set", default_factory=lambda: HashableSequence[Qualifier]()
    )


class PathConstraint(BaseModel):
    """QPath Constraint."""

    intermediate_categories: Annotated[
        Optional[HashableSequence[BiolinkEntity]], AfterValidator(nonzero_validator)
    ]


class SetInterpretationEnum(str, Enum):
    """Enumeration for set interpretation."""

    BATCH = "BATCH"
    ALL = "ALL"
    MANY = "MANY"


class QNode(BaseModel):
    """Query node."""

    ids: Annotated[
        Optional[HashableSequence[CURIE]], AfterValidator(nonzero_validator)
    ] = None
    categories: Annotated[
        Optional[HashableSequence[BiolinkEntity]], AfterValidator(nonzero_validator)
    ] = None
    set_interpretation: Annotated[
        Optional[SetInterpretationEnum], Field(SetInterpretationEnum.BATCH)
    ]
    constraints: HashableSequence[AttributeConstraint] = Field(
        title="attribute constraints",
        default_factory=lambda: HashableSequence[AttributeConstraint](),
    )
    member_ids: Optional[HashableSequence[CURIE]] = Field(
        title="set member ids", default_factory=lambda: HashableSequence[CURIE]()
    )

    model_config = ConfigDict(
        title="query-graph node",
        extra="allow",
        populate_by_name=True,
        use_enum_values=True,  # See https://github.com/pydantic/pydantic/discussions/9270
        validate_default=True,  # See https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.use_enum_values
    )


class QEdge(BaseModel):
    """Query edge."""

    subject: Annotated[
        str,
        Field(
            title="subject node id",
        ),
    ]
    object: Annotated[
        str,
        Field(
            title="object node id",
        ),
    ]
    knowledge_type: Annotated[
        Optional[KnowledgeType], Field(title="knowledge type")
    ] = None
    predicates: Annotated[
        Optional[HashableSequence[BiolinkPredicate]], AfterValidator(nonzero_validator)
    ] = None
    attribute_constraints: HashableSequence[AttributeConstraint] = Field(
        title="attribute constraints",
        default_factory=lambda: HashableSequence[AttributeConstraint](),
    )
    qualifier_constraints: HashableSequence[QualifierConstraint] = Field(
        title="qualifier constraint",
        default_factory=lambda: HashableSequence[QualifierConstraint](),
    )

    model_config = ConfigDict(
        title="query-graph edge", extra="allow", populate_by_name=True
    )


class QPath(BaseModel):
    """Query path."""

    subject: Annotated[
        str,
        Field(
            title="subject node id",
        ),
    ]

    object: Annotated[
        str,
        Field(
            title="object node id",
        ),
    ]

    predicates: Annotated[
        Optional[HashableSequence[BiolinkPredicate]],
        Field(
            title="predicates",
        ),
    ] = None

    constraints: Optional[HashableSequence[PathConstraint]]


class BaseQueryGraph(BaseModel):
    """Base query graph."""

    nodes: Annotated[
        HashableMapping[str, QNode],
        Field(
            title="dict of nodes",
        ),
    ]

    model_config = ConfigDict(title="simple query graph", extra="allow")


class QueryGraph(BaseQueryGraph):
    """Traditional query graph."""

    edges: Annotated[
        HashableMapping[str, QEdge],
        Field(
            title="dict of edges",
        ),
    ]

    model_config = ConfigDict(title="simple query graph", extra="allow")


class PathfinderQueryGraph(BaseQueryGraph):
    """Pathfinder query graph."""

    paths: Annotated[
        HashableMapping[str, QPath],
        Field(
            title="dict of paths",
        ),
    ]

    model_config = ConfigDict(title="pathfinder query graph", extra="allow")
