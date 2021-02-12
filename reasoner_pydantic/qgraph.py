# pylint: disable=too-few-public-methods, missing-class-docstring
"""Query graph models."""
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .shared import BiolinkEntity, BiolinkPredicate, CURIE


class QNode(BaseModel):
    """Query node."""

    id: Union[CURIE, List[CURIE], None] = Field(
        None,
        title='id',
        nullable=True,
    )
    category: Union[BiolinkEntity, List[BiolinkEntity], None] = Field(
        None,
        title='category',
        nullable=True,
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
    predicate: Union[BiolinkPredicate, List[BiolinkPredicate], None] = Field(
        None,
        title='predicate',
        nullable=True,
    )
    relation: Optional[str] = Field(None, nullable=True)

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
