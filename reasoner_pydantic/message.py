"""Reasoner API models."""
from typing import List, Optional

from pydantic import BaseModel, constr, Field

from .results import Result
from .qgraph import QueryGraph
from .kgraph import KnowledgeGraph
from .shared import LogEntry, LogLevel
from .workflow import Workflow


class Message(BaseModel):
    """Message."""

    query_graph: Optional[QueryGraph] = Field(
        None,
        title='query graph',
        nullable=True,
    )
    knowledge_graph: Optional[KnowledgeGraph] = Field(
        None,
        title='knowledge graph',
        nullable=True,
    )
    results: Optional[List[Result]] = Field(
        None,
        title='list of results',
        nullable=True,
    )

    class Config:
        title = 'message'
        extra = 'forbid'


class Query(BaseModel):
    """Request."""

    message: Message = Field(
        ...,
        title='message',
    )
    log_level: Optional[LogLevel] = Field(
        None,
        title='log_level',
        nullable=True,
    )
    workflow: Optional[Workflow]

    class Config:
        title = 'query'
        extra = 'allow'
        schema_extra = {
            "x-body-name": "request_body"
        }


class AsyncQuery(BaseModel):
    """AsyncQuery."""

    callback: constr(regex=r"^https?://") = Field(..., format="uri")
    message: Message = Field(
        ...,
        title='message',
    )
    log_level: Optional[LogLevel] = Field(
        None,
        title='log_level',
        nullable=True,
    )
    workflow: Optional[Workflow]

    class Config:
        title = 'query'
        extra = 'allow'
        schema_extra = {
            "x-body-name": "request_body"
        }


class Response(BaseModel):
    """Response."""

    message: Message = Field(
        ...,
        title='message',
    )

    logs: Optional[List[LogEntry]] = Field(None, nullable=True)

    status: Optional[str] = Field(None, nullable=True)

    workflow: Optional[Workflow]

    class Config:
        title = 'response'
        extra = 'allow'
