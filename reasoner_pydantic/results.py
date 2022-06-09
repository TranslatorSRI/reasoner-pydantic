"""Results models."""
from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .utils import HashableMapping, HashableSet, HashableSetCustomUpdate
from .shared import Attribute, CURIE, InformationResource


class EdgeBindingAttribute(BaseModel):
    """Edge binding attribute"""


class EdgeBinding(BaseModel):
    """Edge binding."""

    id: str = Field(
        ...,
        title="knowledge graph id",
    )

    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "edge binding"
        schema_extra = {
            "example": {
                "id": "string",
            },
        }
        extra = "allow"


class NodeBinding(BaseModel):
    """Node binding."""

    id: CURIE = Field(
        ...,
        title="knowledge graph id",
    )

    class Config:
        title = "node binding"
        schema_extra = {
            "example": {
                "id": "x:string",
            },
        }
        extra = "allow"


class Analysis(BaseModel):
    """Result analysis"""

    resource: InformationResource = Field(
        ..., title="information resource providing the analysis"
    )
    method: Optional[str] = Field(None, title="")
    node_binding_attributes: Optional[
        HashableMapping[str, HashableMapping[str, HashableSet[Attribute]]]
    ]
    edge_binding_attributes: Optional[
        HashableMapping[str, HashableMapping[str, HashableSet[Attribute]]]
    ]
    additional_node_bindings: Optional[
        HashableMapping[str, HashableSet[NodeBinding]]
    ] = Field(
        None,
        title="list of additional node bindings",
    )
    additional_edge_bindings: Optional[
        HashableMapping[str, HashableSet[EdgeBinding]]
    ] = Field(
        None,
        title="list of additional edge bindings",
    )

    score: Optional[float] = Field(None, format="float")

    class Config:
        title = "analysis"
        extra = "allow"


class Result(BaseModel):
    """Result."""

    node_bindings: HashableMapping[str, HashableSet[NodeBinding]] = Field(
        ...,
        title="list of node bindings",
    )
    edge_bindings: HashableMapping[str, HashableSet[EdgeBinding]] = Field(
        ...,
        title="list of edge bindings",
    )
    analyses: Optional[HashableSet[Analysis]] = Field(None, title="list of analyses")

    def __hash__(self) -> int:
        """Hash function based on desired result merging logic"""

        hash_payload = (
            self.node_bindings,
            self.edge_bindings,
        )
        return hash((self.__class__, hash_payload))

    def update(self, other):
        if other.analyses:
            if self.analyses:
                self.analyses.update(other.analyses)
            else:
                self.analyses = other.analyses

    class Config:
        title = "result"
        extra = "allow"


class ResultSet(HashableSetCustomUpdate[Result]):
    """Set of Results"""
