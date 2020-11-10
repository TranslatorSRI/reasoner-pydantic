# pylint: disable=too-few-public-methods, missing-class-docstring
"""Knowledge graph models."""
from typing import Dict, List, Union

from pydantic import BaseModel, Field

from .shared import Attribute, BiolinkEntity, BiolinkRelation, CURIE


class Node(BaseModel):
    """Knowledge graph node."""

    category: Union[BiolinkEntity, List[BiolinkEntity]] = Field(
        None,
        title='category',
    )
    name: str = None
    attributes: List[Attribute] = None

    class Config:
        title = 'knowledge-graph node'
        schema_extra = {
            'example': {
                'category': 'string',
            },
        }
        extra = 'forbid'


class Edge(BaseModel):
    """Knowledge graph edge."""

    subject: CURIE = Field(
        ...,
        title='subject node id',
    )
    object: CURIE = Field(
        ...,
        title='object node id',
    )
    predicate: BiolinkRelation = None
    relation: str = None
    attributes: List[Attribute] = None

    class Config:
        title = 'knowledge-graph edge'
        extra = 'forbid'


class KnowledgeGraph(BaseModel):
    """Knowledge graph."""

    nodes: Dict[str, Node] = Field(
        ...,
        title='nodes',
    )
    edges: Dict[str, Edge] = Field(
        ...,
        title='edges',
    )

    class Config:
        title = 'knowledge graph'
        extra = 'allow'
