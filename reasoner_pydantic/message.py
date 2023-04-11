"""Reasoner API models."""
import hashlib

from typing import Optional, Callable

from pydantic import constr, Field, parse_obj_as

from .base_model import BaseModel
from .utils import HashableSequence, HashableSet
from .results import Result, Results
from .qgraph import QueryGraph
from .kgraph import KnowledgeGraph
from .shared import LogEntry, LogLevel
from .workflow import Workflow
from .auxgraphs import AuxiliaryGraphs


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
    results: Optional[Results] = Field(
        None,
        title="list of results",
        nullable=True,
    )
    auxiliary_graphs: Optional[AuxiliaryGraphs] = Field(
        None, title="list of auxiliary graphs", nullable=True
    )

    class Config:
        title = "message"
        extra = "forbid"

    def parse_obj(obj):
        message = parse_obj_as(Message, obj)
        qgraph = None
        kgraph = None
        results = None
        auxgraphs = None
        if "query_graph" in obj.keys() and obj["query_graph"]:
            qgraph = QueryGraph.parse_obj(obj["query_graph"])
        if "knowledge_graph" in obj.keys() and obj["knowledge_graph"]:
            kgraph = KnowledgeGraph.parse_obj(obj["knowledge_graph"])
        if "results" in obj.keys() and obj["results"]:
            results = Results.parse_obj(obj["results"])
        if "auxiliary_graphs" in obj.keys() and obj["auxiliary_graphs"]:
            auxgraphs = AuxiliaryGraphs.parse_obj(obj["auxiliary_graphs"])
        m = Message(
            query_graph=qgraph,
            knowledge_graph=kgraph,
            results=results,
            auxiliary_graphs=auxgraphs,
        )
        m._normalize_kg_edge_ids()
        m.update(message)
        return m

    def update(self, other: "Message"):
        if hash(self.query_graph) != hash(other.query_graph):
            raise NotImplementedError("Query graph merging not supported yet")
        # Make a copy because normalization will modify results
        other = other.copy(deep=True)

        if other.knowledge_graph:
            if not self.knowledge_graph:
                self.knowledge_graph = KnowledgeGraph(nodes=[], edges=[])
            # Normalize edges of incoming KG
            # This will place KG edge keys into the same hashing system
            # So that equivalence is determined by hash collision
            other._normalize_kg_edge_ids()
            # The knowledge graph can now be udated because edge keys will be
            # hashed using the same method. The knowledge graph update method
            # will handle concatenating properties when necessary.
            self.knowledge_graph.update(other.knowledge_graph)
        if other.results:
            if self.results:
                self.results.update(other.results)
            else:
                self.results = other.results

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
            for result in self.results.__root__:
                if result and result.analyses:
                    for analysis in result.analyses:
                        for edge_binding_list in analysis.edge_bindings.values():
                            for eb in edge_binding_list:
                                eb.id = edge_id_mapping[eb.id]

        # Update auxiliary graphs
        if self.auxiliary_graphs:
            for auxiliary_graph in self.auxiliary_graphs.__root__:
                if auxiliary_graph.edges:
                    for aux_edge in auxiliary_graph.edges:
                        aux_edge = edge_id_mapping[aux_edge]


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
