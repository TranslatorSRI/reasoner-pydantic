# pylint: disable=too-few-public-methods, missing-class-docstring
"""Results models."""
from typing import Dict, List, Union

from pydantic import BaseModel, Field


class EdgeBinding(BaseModel):
    """Edge binding."""

    qg_id: str = Field(
        ...,
        title='query graph id',
    )
    kg_id: Union[str, List[str]] = Field(
        ...,
        title='knowledge graph id',
    )

    class Config:
        title = 'edge binding'
        schema_extra = {
            'example': {
                'qg_id': 'string',
                'kg_id': 'string',
            },
        }
        extra = 'allow'


class NodeBinding(BaseModel):
    """Node binding."""

    qg_id: str = Field(
        ...,
        title='query graph id',
    )
    kg_id: Union[str, List[str]] = Field(
        ...,
        title='knowledge graph id',
    )

    class Config:
        title = 'node binding'
        schema_extra = {
            'example': {
                'qg_id': 'string',
                'kg_id': 'x:string',
            },
        }
        extra = 'allow'


class Result(BaseModel):
    """Result."""

    node_bindings: List[NodeBinding] = Field(
        ...,
        title='list of node bindings',
    )
    edge_bindings: List[EdgeBinding] = Field(
        ...,
        title='list of edge bindings',
    )

    class Config:
        title = 'result'
        extra = 'allow'
