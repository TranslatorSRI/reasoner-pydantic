# pylint: disable=too-few-public-methods, missing-class-docstring
"""Query graph models."""
from typing import Dict, List, Union

from pydantic import BaseModel, Field

from .shared import BiolinkEntity, BiolinkRelation, CURIE


class QNode(BaseModel):
    """Query node."""

    id: Union[CURIE, List[CURIE]] = Field(
        None,
        title='id',
    )
    category: Union[BiolinkEntity, List[BiolinkEntity]] = Field(
        None,
        title='category',
    )
    is_set: bool = False

    class Config:
        title = 'query-graph node'
        extra = 'allow'


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
    predicate: Union[BiolinkRelation, List[BiolinkRelation]] = Field(
        None,
        title='predicate',
    )
    relation: str = None

    class Config:
        title = 'query-graph edge'
        extra = 'allow'


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
