# pylint: disable=too-few-public-methods, missing-class-docstring
"""Reasoner API models."""
from typing import List

from pydantic import BaseModel, Field

from models.results import Result
from models.qgraph import QueryGraph
from models.kgraph import KnowledgeGraph


class Message(BaseModel):
    """Message."""

    query_graph: QueryGraph = Field(
        None,
        title='query graph',
    )
    knowledge_graph: KnowledgeGraph = Field(
        None,
        title='knowledge graph',
    )
    results: List[Result] = Field(
        None,
        title='list of results',
    )

    class Config:
        title = 'message'


class Request(BaseModel):
    """Request."""

    message: Message = Field(
        ...,
        title='message',
    )

    class Config:
        title = 'result'
