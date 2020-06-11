# pylint: disable=too-few-public-methods, missing-class-docstring
"""Knowledge graph models."""
from typing import List, Union

from pydantic import BaseModel, constr, Field

CURIE = constr(regex='^.+:.+$')


class KNode(BaseModel):
    """Knowledge graph node."""

    id: Union[CURIE, List[CURIE]] = Field(
        ...,
        title='id',
    )
    type: str = Field(
        None,
        title='type',
    )

    class Config:
        title = 'knowledge-graph node'
        schema_extra = {
            'example': {
                'id': 'x:string',
                'type': 'string',
            },
        }
        extra = 'allow'


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
        extra = 'allow'


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
        extra = 'allow'
