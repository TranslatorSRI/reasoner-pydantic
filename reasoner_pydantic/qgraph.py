"""Query graph models."""
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field
from pydantic.types import conlist

from .shared import BiolinkEntity, BiolinkPredicate, CURIE


class Operator(str, Enum):
    """Operator."""
    equal_to = '=='
    greater_than = '>'
    less_than = '<'
    matches = 'matches'


class QueryConstraint(BaseModel):
    """QNode or QEdge constraint."""
    name: str = Field(
        ...,
        title='name',
        nullable=False,
    )
    id: CURIE = Field(
        ...,
        title='id',
        nullable=False,
    )
    negated: bool = Field(
        False,
        title='not',
        alias='not',
    )
    operator: Operator = Field(
        ...,
        title='operator',
    )
    value: Any = Field(
        ...,
        title='value',
    )
    unit_id: Optional[Any] = Field(
        None,
        title='unit_id',
    )
    unit_name: Optional[Any] = Field(
        None,
        title='unit_name',
    )

    class Config:
        extra = 'forbid'

    def dict(self, *args, **kwargs):
        output = super().dict(*args, **kwargs)
        output['not'] = output.pop('negated', False)
        return output


class QNode(BaseModel):
    """Query node."""

    ids: Optional[conlist(CURIE, min_items=1)] = Field(
        None,
        title='ids',
        nullable=True,
    )
    categories: Optional[conlist(BiolinkEntity, min_items=1)] = Field(
        None,
        title='categories',
        nullable=True,
    )
    is_set: bool = False
    constraints: Optional[List[QueryConstraint]] = Field(
        None,
        title='constraints',
        nullable=True,
    )

    class Config:
        title = 'query-graph node'
        extra = 'allow'
        allow_population_by_field_name = True


class QEdge(BaseModel):
    """Query edge."""

    subject: str = Field(
        ...,
        title='subject node id',
    )
    object: str = Field(
        ...,
        title='object node id',
    )
    predicates: Union[conlist(BiolinkPredicate, min_items=1), None] = Field(
        None,
        title='predicates',
        nullable=True,
    )
    constraints: Optional[List[QueryConstraint]] = Field(
        None,
        title='constraints',
        nullable=True,
    )

    class Config:
        title = 'query-graph edge'
        extra = 'allow'
        allow_population_by_field_name = True


class QueryGraph(BaseModel):
    """Query graph."""

    nodes: Dict[str, QNode] = Field(
        ...,
        title='dict of nodes',
    )
    edges: Dict[str, QEdge] = Field(
        ...,
        title='dict of edges',
    )

    class Config:
        title = 'simple query graph'
        extra = 'allow'
