"""Results models."""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .shared import Attribute, CURIE


class EdgeBinding(BaseModel):
    """Edge binding."""

    id: str = Field(
        ...,
        title='knowledge graph id',
    )

    attributes: Optional[List[Attribute]] = Field(None, nullable=True)

    class Config:
        title = 'edge binding'
        schema_extra = {
            'example': {
                'id': 'string',
            },
        }
        extra = 'allow'


class NodeBinding(BaseModel):
    """Node binding."""

    id: CURIE = Field(
        ...,
        title='knowledge graph id',
    )

    class Config:
        title = 'node binding'
        schema_extra = {
            'example': {
                'id': 'x:string',
            },
        }
        extra = 'allow'


class Result(BaseModel):
    """Result."""

    node_bindings: Dict[str, List[NodeBinding]] = Field(
        ...,
        title='list of node bindings',
    )
    edge_bindings: Dict[str, List[EdgeBinding]] = Field(
        ...,
        title='list of edge bindings',
    )
    score: Optional[float] = Field(
        None,
        format="float",
    )

    class Config:
        title = 'result'
        extra = 'allow'
