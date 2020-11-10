"""Reasoner-pydantic module."""

from .kgraph import KnowledgeGraph, Node, Edge
from .qgraph import QueryGraph, QNode, QEdge
from .results import Result, NodeBinding, EdgeBinding
from .message import Message, Query, Response
from .shared import Attribute, BiolinkEntity, BiolinkRelation, CURIE, LogEntry

components = [
    Attribute,
    BiolinkEntity, BiolinkRelation, CURIE,
    Edge, EdgeBinding,
    KnowledgeGraph, LogEntry, Message,
    Node, NodeBinding,
    QEdge, QNode,
    Query, QueryGraph,
    Result,
]
