"""Auxiliary Graphs model"""
from typing import Optional

from pydantic import Field, parse_obj_as

from .base_model import BaseModel
from .utils import HashableMapping, HashableSet
from .shared import Attribute, CURIE


class AuxiliaryGraph(BaseModel):
    """Auxiliary Graph"""

    edges: HashableSet[str] = Field(..., title="edges in auxiliary graph")

    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "auxiliary graph"
        extra = "allow"


class AuxiliaryGraphs(BaseModel):
    """Auxiliary Graphs"""

    __root__: Optional[HashableSet[AuxiliaryGraph]]

    class Config:
        title = "auxiliary graphs"
        extra = "allow"

    def add(self, graph):
        self.__root__.add(graph)

    def update(self, other):
        self.__root__.update(other.__root__)

    def parse_obj(obj):
        auxiliary_graphs = parse_obj_as(AuxiliaryGraphs, obj)
        graphs = AuxiliaryGraphs()
        graphs.__root__ = HashableSet[AuxiliaryGraph]()
        for graph in obj:
            graphs.add(AuxiliaryGraph.parse_obj(graph))
        return graphs.update(auxiliary_graphs)
