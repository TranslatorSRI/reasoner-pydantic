"""Knowledge graph models."""
from typing import Optional, Union

from pydantic import Field

from .shared import Attribute, BiolinkEntity, BiolinkPredicate, CURIE
from .base_model import BaseModel
from .utils import HashableMapping, HashableSequence


class Node(BaseModel):
    """Knowledge graph node."""

    categories: Optional[HashableSequence[BiolinkEntity]] = Field(
        None,
        title="categories",
        nullable=True,
    )
    name: Optional[str] = Field(None, nullable=True)
    attributes: Optional[HashableSequence[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "knowledge-graph node"
        schema_extra = {
            "example": {
                "category": "string",
            },
        }
        extra = "forbid"
        allow_population_by_field_name = True


class Edge(BaseModel):
    """Knowledge graph edge."""

    subject: CURIE = Field(
        ...,
        title="subject node id",
    )
    object: CURIE = Field(
        ...,
        title="object node id",
    )
    predicate: Optional[BiolinkPredicate] = Field(None, nullable=True)
    attributes: Optional[HashableSequence[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "knowledge-graph edge"
        extra = "forbid"


class KnowledgeGraph(BaseModel):
    """Knowledge graph."""

    nodes: HashableMapping[str, Node] = Field(
        ...,
        title="nodes",
    )
    edges: HashableMapping[str, Edge] = Field(
        ...,
        title="edges",
    )

    class Config:
        title = "knowledge graph"
        extra = "allow"
