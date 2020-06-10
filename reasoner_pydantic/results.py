# pylint: disable=too-few-public-methods
"""Results models."""
from typing import Dict, List, Union

from pydantic import BaseModel, constr, Field

CURIE = constr(regex='^.+:.+$')


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


class NodeBinding(BaseModel):
    """Node binding."""

    qg_id: str = Field(
        ...,
        title='query graph id',
    )
    kg_id: Union[CURIE, List[CURIE]] = Field(
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
    extra_nodes: List[Dict] = Field(
        None,
        title='list of extra nodes',
    )
    extra_edges: List[Dict] = Field(
        None,
        title='list of extra edges',
    )

    class Config:
        title = 'result'
