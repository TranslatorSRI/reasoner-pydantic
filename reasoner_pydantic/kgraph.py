# pylint: disable=too-few-public-methods, missing-class-docstring
"""Knowledge graph models."""
from typing import List, Union

from pydantic import BaseModel, constr, Field

CURIE = constr(regex='^.+:.+$')


class KNode(BaseModel):
    """Knowledge graph node."""

    id: str = Field(
        ...,
        title='id',
    )
    type: Union[CURIE, List[CURIE]] = Field(
        None,
        title='type',
    )

    class Config:
        title = 'knowledge-graph node'


class KEdge(BaseModel):
    """Knowledge graph edge."""

    id: str = Field(
        ...,
        title='identifier',
    )
    source_id: str = Field(
        ...,
        title='source node id',
    )
    target_id: str = Field(
        ...,
        title='target node id',
    )
    type: Union[str, List[str]] = None

    class Config:
        title = 'knowledge-graph edge'


class KnowledgeGraph(BaseModel):
    """Knowledge graph."""

    nodes: List[KNode] = Field(
        ...,
        title='nodes',
    )
    edges: List[KEdge] = Field(
        ...,
        title='edges',
    )

    class Config:
        title = 'knowledge graph'
