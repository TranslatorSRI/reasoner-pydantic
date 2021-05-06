"""Query graph models."""
from typing import Dict, List, Optional, Union

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic.types import conlist

from .shared import BiolinkEntity, BiolinkPredicate, CURIE


def listify(str_or_list: Union[str, List[str]]):
    """Ensure that string is enclosed in list."""
    if str_or_list is None:
        return None
    if not isinstance(str_or_list, list):
        return [str_or_list]
    return str_or_list


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


class QNode(BaseModel):
    """Query node."""

    id: Optional[conlist(CURIE, min_items=1)] = Field(
        None,
        title='id',
        nullable=True,
        alias='ids',
    )
    category: Optional[conlist(BiolinkEntity, min_items=1)] = Field(
        None,
        title='category',
        nullable=True,
        alias='categories',
    )
    is_set: bool = False
    constraints: Optional[List[QueryConstraint]] = Field(
        None,
        title='constraints',
        nullable=True,
    )
    
    _listify_categories = validator(
        "category",
        allow_reuse=True,
        pre=True,
    )(listify)
    _listify_ids = validator(
        "id",
        allow_reuse=True,
        pre=True,
    )(listify)

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
    predicate: Union[conlist(BiolinkPredicate, min_items=1), None] = Field(
        None,
        title='predicate',
        nullable=True,
        alias='predicates',
    )
    relation: Optional[str] = Field(None, nullable=True)
    constraints: Optional[List[QueryConstraint]] = Field(
        None,
        title='constraints',
        nullable=True,
    )

    _listify_predicates = validator(
        "predicate",
        allow_reuse=True,
        pre=True,
    )(listify)

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
