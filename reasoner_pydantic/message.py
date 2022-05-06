"""Reasoner API models."""
import hashlib

from typing import Optional, Callable

from pydantic import constr, Field

from .base_model import BaseModel
from .utils import HashableSequence, HashableSet
from .results import Result
from .qgraph import QueryGraph
from .kgraph import KnowledgeGraph
from .shared import LogEntry, LogLevel
from .workflow import Workflow


class Message(BaseModel):
    """Message."""

    query_graph: Optional[QueryGraph] = Field(
        None,
        title="query graph",
        nullable=True,
    )
    knowledge_graph: Optional[KnowledgeGraph] = Field(
        None,
        title="knowledge graph",
        nullable=True,
    )
    results: Optional[HashableSet[Result]] = Field(
        None,
        title="list of results",
        nullable=True,
    )

    class Config:
        title = "message"
        extra = "forbid"

    def update(self, other: "Message"):
        if hash(self.query_graph) != hash(other.query_graph):
            raise NotImplementedError("Query graph merging not supported yet")
        # Make a copy because normalization will modify results
        other = other.copy(deep=True)

        if other.knowledge_graph:
            if not self.knowledge_graph:
                self.knowledge_graph = KnowledgeGraph(nodes=[], edges=[])
            # Normalize edges of incoming KG
            other._normalize_kg_edge_ids()
            self.knowledge_graph.update(other.knowledge_graph)
        if other.results:
            if not self.results:
                self.results = HashableSet[Result]()
            self.results.update(other.results)

    def _normalize_kg_edge_ids(self):
        """
        Replace edge IDs with a hash of the edge object
        """
        self._update_kg_edge_ids(
            lambda edge: hashlib.blake2b(
                hash(edge).to_bytes(16, byteorder="big", signed=True), digest_size=6
            ).hexdigest(),
        )

    def _update_kg_edge_ids(self, update_func: Callable):
        """
        Replace edge IDs using the specified function
        """

        # Mapping of old to new edge IDs
        edge_id_mapping = {}

        # Make a copy of the edge keys because we're about to change them
        for edge_id in list(self.knowledge_graph.edges.keys()):
            edge = self.knowledge_graph.edges.pop(edge_id)
            new_edge_id = update_func(edge)

            edge_id_mapping[edge_id] = new_edge_id

            # Update knowledge graph
            self.knowledge_graph.edges[new_edge_id] = edge

        # Update results
        if self.results:
            for result in self.results:
                for edge_binding_list in result.edge_bindings.values():
                    for eb in edge_binding_list:
                        eb.id = edge_id_mapping[eb.id]


class Query(BaseModel):
    """Request."""

    message: Message = Field(
        ...,
        title="message",
    )
    log_level: Optional[LogLevel] = Field(
        None,
        title="log_level",
        nullable=True,
    )
    workflow: Optional[Workflow]

    class Config:
        title = "query"
        extra = "allow"
        schema_extra = {"x-body-name": "request_body"}


class AsyncQuery(BaseModel):
    """AsyncQuery."""

    callback: constr(regex=r"^https?://") = Field(..., format="uri")
    message: Message = Field(
        ...,
        title="message",
    )
    log_level: Optional[LogLevel] = Field(
        None,
        title="log_level",
        nullable=True,
    )
    workflow: Optional[Workflow]

    class Config:
        title = "query"
        extra = "allow"
        schema_extra = {"x-body-name": "request_body"}


class Response(BaseModel):
    """Response."""

    message: Message = Field(
        ...,
        title="message",
    )

    logs: Optional[HashableSequence[LogEntry]] = Field(None, nullable=True)

    status: Optional[str] = Field(None, nullable=True)

    workflow: Optional[Workflow]

    class Config:
        title = "response"
        extra = "allow"
