# pylint: disable=too-few-public-methods, missing-class-docstring
"""Query graph models."""
from typing import List, Union

from pydantic import BaseModel, constr, Field

CURIE = constr(regex='^.+:.+$')


class QNode(BaseModel):
    """Query node."""

    id: str = Field(
        ...,
        title='id',
    )
    curie: Union[CURIE, List[CURIE]] = Field(
        None,
        title='CURIE',
    )
    type: Union[str, List[str]] = Field(
        None,
        title='type',
    )

    class Config:
        title = 'query-graph node'
        extra = 'allow'


class QEdge(BaseModel):
    """Query edge."""

    id: str = Field(
        ...,
        title='id',
    )
    source_id: str = Field(
        ...,
        title='source node id',
    )
    target_id: str = Field(
        ...,
        title='target node id',
    )
    type: Union[str, List[str]] = Field(
        None,
        title='type',
    )

    class Config:
        title = 'query-graph edge'
        extra = 'allow'


class QueryGraph(BaseModel):
    """Query graph."""

    nodes: List[QNode] = Field(
        ...,
        title='list of nodes',
    )
    edges: List[QEdge] = Field(
        ...,
        title='list of edges',
    )

    class Config:
        title = 'simple query graph'
        extra = 'allow'
