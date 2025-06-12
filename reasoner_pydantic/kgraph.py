"""Knowledge graph models."""

from typing import Annotated, Any, Optional

from pydantic import ConfigDict, Field

from .shared import (
    Attribute,
    BiolinkEntity,
    BiolinkPredicate,
    CURIE,
    EdgeIdentifier,
    Qualifier,
    ResourceRoleEnum,
)
from .base_model import BaseModel
from .utils import HashableMapping, HashableSet


class Node(BaseModel):
    """Knowledge graph node."""

    categories: HashableSet[BiolinkEntity]
    name: Optional[str] = None
    attributes: HashableSet[Attribute]
    is_set: Optional[bool] = None

    model_config = ConfigDict(
        title="knowledge-graph node",
        json_schema_extra={
            "example": {
                "category": "string",
            },
        },
        extra="forbid",
        populate_by_name=True,
    )

    def update(self, other: object) -> None:
        if not isinstance(other, Node):
            raise TypeError("Node may only be updated with Node.")
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


class RetrievalSource(BaseModel):
    """A component of source retrieval provenance"""

    resource_id: Annotated[CURIE, Field(title="infores for source")]
    resource_role: Annotated[ResourceRoleEnum, Field(title="source type")]
    upstream_resource_ids: Optional[HashableSet[CURIE]] = None
    source_record_urls: Optional[HashableSet[str]] = None

    def __hash__(self) -> int:
        return hash((self.resource_id, self.resource_role))

    def update(self, other: object):
        if not isinstance(other, RetrievalSource):
            raise TypeError("RetrievalSource may only be updated with RetrievalSource.")
        if other.upstream_resource_ids:
            if self.upstream_resource_ids:
                self.upstream_resource_ids.update(other.upstream_resource_ids)
            else:
                self.upstream_resource_ids = other.upstream_resource_ids


class Edge(BaseModel):
    """Knowledge graph edge."""

    subject: Annotated[
        CURIE,
        Field(
            title="subject node id",
        ),
    ]
    object: Annotated[
        CURIE,
        Field(
            title="object node id",
        ),
    ]
    predicate: Annotated[BiolinkPredicate, Field(title="edge predicate")]
    sources: Annotated[
        HashableSet[RetrievalSource], Field(title="list of source retrievals")
    ]
    qualifiers: Optional[HashableSet[Qualifier]] = None
    attributes: Optional[HashableSet[Attribute]]

    model_config = ConfigDict(title="knowledge-graph edge", extra="forbid")

    def __hash__(self) -> int:
        primary_knowledge_source = self.get_primary_knowedge_source()
        return hash(
            (
                self.subject,
                self.object,
                self.predicate,
                self.qualifiers,
                primary_knowledge_source,
            )
        )

    def update(self, other: Any):
        if not isinstance(other, Edge):
            raise TypeError("Edge may only be updated with Edge.")
        if other.attributes:
            if self.attributes:
                # We need to make sure we don't add a second KL/AT
                new_attributes = HashableSet[Attribute](set())
                for attribute in other.attributes:
                    if attribute.attribute_type_id not in (
                        "biolink:knowledge_level",
                        "biolink:agent_type",
                    ):
                        new_attributes.add(attribute)
                self.attributes.update(new_attributes)
            else:
                self.attributes = other.attributes
        if other.sources:
            if self.sources:
                # We need to do the union of the two sets and then update each
                # source with the information from the other list
                self.sources.update(other.sources)
                for source in self.sources:
                    for other_source in other.sources:
                        if source == other_source:
                            source.update(other_source)
            else:
                self.sources = other.sources

    def get_primary_knowedge_source(self):
        for source in self.sources:
            if source.resource_role == "primary_knowledge_source":
                return source.resource_id


class KnowledgeGraph(BaseModel):
    """Knowledge graph."""

    nodes: HashableMapping[CURIE, Node] = Field(
        default_factory=lambda: HashableMapping[CURIE, Node]()
    )
    edges: HashableMapping[EdgeIdentifier, Edge] = Field(
        default_factory=lambda: HashableMapping[EdgeIdentifier, Edge]()
    )

    model_config = ConfigDict(title="knowledge graph", extra="allow")

    def update(self, other: object) -> None:
        if not isinstance(other, KnowledgeGraph):
            raise TypeError("KnowledgeGraph may only be updated with KnowledgeGraph.")

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
