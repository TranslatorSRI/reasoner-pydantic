"""Reasoner API models."""
import hashlib

from typing import Optional, Callable

from pydantic import constr, Field

from .base_model import BaseModel
from .utils import HashableSequence, HashableSet, HashableSetCustomUpdate
from .results import Result
from .qgraph import QueryGraph
from .kgraph import KnowledgeGraph
from .shared import LogEntry, LogLevel
from .workflow import Workflow
from .upgrade import upgrade_from_1p2


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
    results: Optional[HashableSetCustomUpdate[Result]] = Field(
        None,
        title="list of results",
        nullable=True,
    )

    class Config:
        title = "message"
        extra = "forbid"

    def update(self, other: "Message"):
        if self.query_graph:
            if hash(self.query_graph) != hash(other.query_graph):
                # In practice this could be support but many decisions wouldn't need to be made
                # For example must qnode keys match? Or is topology sufficient?
                raise NotImplementedError("Query graph merging not supported")
        else:
            # To support merging with empty
            self.query_graph = other.query_graph

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

        # After updating edge keys above all results will reference the new edge
        # keys. Results can be updated directly. The Result update method will
        # handle concatenating properties when necessary.
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

        # Update results to reference the new keys
        if self.results:
            for result in self.results:
                for edge_binding_list in result.edge_bindings.values():
                    for eb in edge_binding_list:
                        eb.id = edge_id_mapping[eb.id]

    @staticmethod
    def merge(*args):
        m = Message()
        for a in args:
            m.update(Message.parse_obj(a))
        return m

    @staticmethod
    def upgrade(from_ver, old_dict, **kwargs):
        upgrades = {"1.2": upgrade_from_1p2}
        if from_ver in upgrades.keys():
            return Message.parse_obj(upgrades[from_ver](old_dict, **kwargs))
        else:
            raise Exception(
                f"Unknown upgradeable version {from_ver}. Options: {upgrades.keys()}"
            )


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
