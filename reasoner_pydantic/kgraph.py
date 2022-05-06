"""Knowledge graph models."""
from typing import Optional

from pydantic import Field

from .shared import Attribute, BiolinkEntity, BiolinkPredicate, CURIE, EdgeIdentifier
from .base_model import BaseModel
from .utils import HashableMapping, HashableSet


class Node(BaseModel):
    """Knowledge graph node."""

    categories: Optional[HashableSet[BiolinkEntity]] = Field(
        None,
        title="categories",
        nullable=True,
    )
    name: Optional[str] = Field(None, nullable=True)
    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "knowledge-graph node"
        schema_extra = {
            "example": {
                "category": "string",
            },
        }
        extra = "forbid"
        allow_population_by_field_name = True

    def update(self, other):
        if other.name:
            self.name = other.name

        if other.categories:
            if self.categories:
                self.categories.update(other.categories)
            else:
                self.categories = other.categories

        if other.attributes:
            if self.attributes:
                self.attributes.update(other.attributes)
            else:
                self.attributes = other.attributes


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
    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "knowledge-graph edge"
        extra = "forbid"

    def update(self, other):
        if other.attributes:
            if self.attributes:
                self.attributes.update(other.attributes)
            else:
                self.attributes = other.attributes


class KnowledgeGraph(BaseModel):
    """Knowledge graph."""

    nodes: HashableMapping[CURIE, Node] = Field(
        ...,
        title="nodes",
    )
    edges: HashableMapping[EdgeIdentifier, Edge] = Field(
        ...,
        title="edges",
    )

    class Config:
        title = "knowledge graph"
        extra = "allow"

    def update(self, other):
        for key, value in other.nodes.items():
            existing = self.nodes.get(key, None)
            if existing:
                existing.update(value)
            else:
                self.nodes[key] = value

        for key, value in other.edges.items():
            existing = self.edges.get(key, None)
            if existing:
                existing.update(value)
            else:
                self.edges[key] = value
