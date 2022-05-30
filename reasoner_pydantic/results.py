"""Results models."""
from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .utils import HashableMapping, HashableSet
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

    source: InformationResource = Field(..., title="list of node bindings")
    methdod: Optional[str] = Field(None, title="")
    node_binding_attributes: Optional[HashableMapping[str, HashableSet[Attribute]]]
    edge_binding_attributes: Optional[HashableMapping[str, HashableSet[Attribute]]]

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
    
    class Config:
        title = "result"
        extra = "allow"
