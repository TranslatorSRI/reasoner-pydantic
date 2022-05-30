"""Knowledge graph models."""
from re import L
from typing import Optional

from pydantic import Field

from .shared import Attribute, BiolinkEntity, BiolinkPredicate, CURIE, EdgeIdentifier, InformationResource
from .base_model import BaseModel
from .utils import HashableMapping, HashableSequence, HashableSet


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

# For now qualifiers are unvalidated
class Qualifier(BaseModel):
    """Knowledge graph edge qualifier."""
    class Config:
        title = "knowledge-graph edge qualifier"
        extra = "allow"

class EdgeRetrieval(BaseModel):
    """Knowledge graph edge retrieval"""

    retrieved_from: InformationResource = Field(..., title="type")
    retrieval_method: Optional[str] = Field(None, nullable=True)
    retrieval_date: Optional[str] = Field(None, nullable=True)
    retrieval_version: Optional[str] = Field(None, nullable=True)
    retrieved_by: Optional[str] = Field(None, nullable=True)
    access_url: Optional[str] = Field(None, nullable=True)
    
    
    class Config:
        title = "knowledge-graph edge retrieval"
        extra = "allow"

class EdgeSource(BaseModel):
    """Knowledge graph edge soruce"""
    
    resource: InformationResource = Field(..., title="type")
    resource_role: Optional[str] = Field(None, nullable=True) 
    retrievals: Optional[HashableSet[EdgeRetrieval]] = Field(None, nullabled=True)
    class Config:
        title = "knowledge-graph edge source"
        extra = "allow"
    
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
    negated: Optional[bool] = Field(None, nullable=True)
    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)
    qualifiers: Optional[HashableSet[Qualifier]] = Field(None, nullable=True)
    sources: Optional[HashableSet[EdgeSource]] = Field(None, nullable=True)

    class Config:
        title = "knowledge-graph edge"
        extra = "forbid"

    def update(self, other):
        if other.sources:
            if self.sources:
                self.sources.update(other.sources)
            else:
                self.sources = other.sources
        if other.attributes:
            if self.attributes:
                self.attributes.update(other.attributes)
            else:
                self.attributes = other.attributes

    def __hash__(self) -> int:
        """Hash function based on desired edge merging logic"""
        desired_knowledge_source = ''
        if self.sources:
            for s in self.sources:
                if s.resource_role == 'biolink:original_knowledge_source':
                    desired_knowledge_source = s
                    break
                if s.resource_role == 'biolink:primary_knowledge_source':
                    desired_knowledge_source = s
                    break

        hash_payload = (
            self.subject,
            self.object,
            self.predicate,
            self.qualifiers,
            self.negated,
            desired_knowledge_source,
        )
        return hash((self.__class__, hash_payload))


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
