"""Reasoner API models."""
from typing import Optional, Set

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

    def update(self, other):
        if hash(self.query_graph) != hash(other.query_graph):
            raise NotImplementedError("Query graph merging not supported yet")
        if other.knowledge_graph:
            if not self.knowledge_graph:
                self.knowledge_graph = KnowledgeGraph(nodes=[], edges=[])
            self.knowledge_graph.update(other.knowledge_graph)
        if other.results:
            self.results.update(other.results)


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
