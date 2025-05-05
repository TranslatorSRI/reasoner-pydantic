"""Reasoner API models."""

import copy
import hashlib

from typing import Optional, Callable, Union


from .results import Result, Results, Analysis
from .qgraph import QueryGraph, PathfinderQueryGraph
from pydantic import (
    AnyHttpUrl,
    ValidationInfo,
    ConfigDict,
    Field,
    model_validator,
)

from .base_model import BaseModel
from .utils import HashableSequence
from .results import Results
from .qgraph import QueryGraph
from .kgraph import Edge, KnowledgeGraph
from .shared import EdgeIdentifier, LogEntry, LogLevel
from .workflow import Workflow
from .auxgraphs import AuxiliaryGraphs
from typing import Annotated


class Message(BaseModel):
    """Message."""


    query_graph: Annotated[
        Optional[Union[QueryGraph PathfinderQueryGraph]],
        Field(
            title="query graph",
        ),
    ] = None
    # query_graph: Optional[QueryGraph] = None
    knowledge_graph: Annotated[
        Optional[KnowledgeGraph],
        Field(
            title="knowledge graph",
        ),
    ] = None
    results: Annotated[
        Optional[Results],
        Field(
            title="list of results",
        ),
    ] = None
    auxiliary_graphs: Annotated[
        Optional[AuxiliaryGraphs],
        Field(
            title="dict of auxiliary graphs",
        ),
    ] = None
    model_config = ConfigDict(title="message", extra="forbid")

    def update(self, other: object, normalize: bool = True) -> None:
        """Updates one message with information from another.
        Can run with normalize=false, if both messages are normalized already."""
        if not isinstance(other, Message):
            raise TypeError("Message may only be updated with another Message.")

        if hash(self.query_graph) != hash(other.query_graph):
            raise NotImplementedError("Query graph merging not supported yet")
        # Make a copy because normalization will modify results
        other = other.model_copy(deep=True)

        if other.knowledge_graph:
            if not self.knowledge_graph:
                self.knowledge_graph = KnowledgeGraph()
            # Normalize edges of incoming KG
            # This will place KG edge keys into the same hashing system
            # So that equivalence is determined by hash collision
            if normalize:
                other._normalize_kg_edge_ids()
            # The knowledge graph can now be updated because edge keys will be
            # hashed using the same method. The knowledge graph update method
            # will handle concatenating properties when necessary.
            self.knowledge_graph.update(other.knowledge_graph)
        if other.results:
            if self.results:
                self.results.update(other.results)
            else:
                self.results = other.results
        if other.auxiliary_graphs:
            if self.auxiliary_graphs:
                self.auxiliary_graphs.update(other.auxiliary_graphs)
            else:
                self.auxiliary_graphs = other.auxiliary_graphs

    @model_validator(mode="after")
    def normalize_on_parse(self, info: ValidationInfo) -> "Message":
        normalize = True
        if isinstance(info.context, dict) and not info.context.get("normalize", True):
            normalize = False
        if normalize and self.knowledge_graph is not None:
            self._normalize_kg_edge_ids()
        return self

    def normalize(self) -> None:
        self._normalize_kg_edge_ids()

    def _normalize_kg_edge_ids(self) -> None:
        """
        Replace edge IDs with a hash of the edge object
        """
        self._update_kg_edge_ids(
            lambda edge: EdgeIdentifier.model_validate(
                hashlib.blake2b(
                    hash(edge).to_bytes(16, byteorder="big", signed=True), digest_size=6
                ).hexdigest()
            )
        )

    def _update_kg_edge_ids(self, update_func: Callable[[Edge], EdgeIdentifier]):
        """
        Replace edge IDs using the specified function
        """

        if self.knowledge_graph is None:
            return

        # Mapping of old to new edge IDs
        edge_id_mapping: dict[EdgeIdentifier, EdgeIdentifier] = {}

        # Make a copy of the edge keys because we're about to change them
        for edge_id in list(self.knowledge_graph.edges.keys()):
            edge = self.knowledge_graph.edges.pop(edge_id)
            new_edge_id = update_func(edge)

            edge_id_mapping[edge_id] = new_edge_id

            # Update knowledge graph
            self.knowledge_graph.edges[new_edge_id] = edge

        # Update auxiliary graphs
        if self.auxiliary_graphs:
            aux_len = len(self.auxiliary_graphs.values())
            aux_num = 0
            for auxiliary_graph in self.auxiliary_graphs.values():
                aux_num += 1
                if auxiliary_graph.edges:
                    edges_len = len(auxiliary_graph.edges)
                    edges_num = 0
                    aux_edges = copy.deepcopy(auxiliary_graph.edges)
                    for aux_edge in aux_edges:
                        edges_num += 1
                        auxiliary_graph.edges.discard(aux_edge)
                        try:
                            new_edge_id = edge_id_mapping[aux_edge]
                            auxiliary_graph.edges.add(new_edge_id)
                            edge_id_mapping[new_edge_id] = new_edge_id
                        except KeyError:
                            raise Exception(
                                f"Aux graph edge id {aux_edge} not found in edge id mapping"
                            )
                    if edges_len != edges_num:
                        raise Exception("Missed an aux graph edge normalization.")
                else:
                    raise Exception("This aux graph has no edges")
            if aux_len != aux_num:
                raise Exception("Missed an aux graph normalization.")

        # Update results
        if self.results:
            for result in self.results:
                if result and result.analyses:
                    for analysis in result.analyses:
                        if isinstance(analysis, Analysis):
                            for edge_binding_list in analysis.edge_bindings.values():
                                for eb in edge_binding_list:
                                    eb.id = edge_id_mapping[eb.id]


class Query(BaseModel):
    """Request."""

    message: Message
    log_level: Optional[LogLevel] = None
    workflow: Optional[Workflow] = None
    bypass_cache: Optional[bool] = False
    model_config = ConfigDict(
        title="query", extra="allow", json_schema_extra={"x-body-name": "request_body"}
    )


class AsyncQuery(BaseModel):
    """AsyncQuery."""

    callback: AnyHttpUrl
    message: Message
    log_level: Optional[LogLevel] = None
    workflow: Optional[Workflow] = None
    bypass_cache: Optional[bool] = False
    model_config = ConfigDict(
        title="query", extra="allow", json_schema_extra={"x-body-name": "request_body"}
    )


class Response(BaseModel):
    """Response."""

    message: Message
    logs: HashableSequence[LogEntry] = Field(
        default_factory=lambda: HashableSequence[LogEntry]()
    )
    status: Optional[str] = None
    description: Optional[str] = None
    workflow: Optional[Workflow] = None
    schema_verison: Optional[str] = None
    biolink_version: Optional[str] = None

    model_config = ConfigDict(title="response", extra="allow")

    @model_validator(mode="after")
    def normalize(self, info: ValidationInfo) -> "Response":
        normalize = True
        if isinstance(info.context, dict) and not info.context.get("normalize", True):
            normalize = False
        if normalize and self.message.knowledge_graph is not None:
            self.message.normalize()
        return self


class AsyncQueryResponse(BaseModel):
    """ "Async Query Response."""

    status: Optional[str] = None
    description: Optional[str] = None
    job_id: Annotated[str, Field(title="job id")]
    model_config = ConfigDict(title="async query response", extra="allow")


class AsyncQueryStatusResponse(BaseModel):
    """Async Query Status Response."""

    status: str
    description: str
    logs: HashableSequence[LogEntry]
    response_url: Optional[str] = None

    model_config = ConfigDict(title="async query status response", extra="allow")
