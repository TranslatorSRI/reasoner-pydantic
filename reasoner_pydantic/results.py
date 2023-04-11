"""Results models."""
from typing import Optional

from pydantic import Field, parse_obj_as

from .base_model import BaseModel
from .utils import HashableMapping, HashableSet
from .shared import Attribute, CURIE


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


class Analysis(BaseModel):
    """Analysis."""

    resource_id: CURIE = Field(
        ...,
        title="resource infores",
    )

    edge_bindings: HashableMapping[str, HashableSet[EdgeBinding]] = Field(
        ...,
        title="list of edge bindings",
    )

    score: Optional[float] = Field(
        None,
        format="float",
    )

    support_graphs: Optional[HashableSet[str]] = Field(None, nullable=True)

    scoring_method: Optional[str] = Field(None, nullable=True)

    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "analysis"
        extra = "allow"

    def __hash__(self) -> int:
        return hash(
            (
                self.resource_id,
                self.edge_bindings,
                self.score,
                self.support_graphs,
                self.scoring_method,
            )
        )

    def update(self, other):
        if other.attributes:
            if self.attributes:
                self.attributes.update(other.attributes)
            else:
                self.attributes = other.attributes


class NodeBinding(BaseModel):
    """Node binding."""

    id: CURIE = Field(
        ...,
        title="knowledge graph id",
    )

    query_id: Optional[CURIE] = Field(None, title="query graph id")

    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)

    class Config:
        title = "node binding"
        schema_extra = {
            "example": {
                "id": "x:string",
            },
        }
        extra = "allow"


class Result(BaseModel):
    """Result."""

    node_bindings: HashableMapping[str, HashableSet[NodeBinding]] = Field(
        ...,
        title="list of node bindings",
    )

    analyses: Optional[HashableSet[Analysis]] = Field(
        None, title="list of anlysis blocks", nullable=True
    )

    class Config:
        title = "result"
        extra = "allow"

    def update(self, other):
        if other.analyses:
            if self.analyses:
                for analysis in other.analyses:
                    check = True
                    for ana in self.analyses:
                        if analysis == ana:
                            ana.update(analysis)
                            check = False
                    if check:
                        self.analyses.add(analysis)
            else:
                self.analyses = other.analyses

    def __hash__(self) -> int:
        return hash(self.node_bindings)

    def parse_obj(obj):
        result = parse_obj_as(Result, obj)
        nbindings = HashableMapping.parse_obj(obj["node_bindings"])
        analyses = HashableSet[Analysis]()
        if "analyses" in obj.keys():
            for analysis in obj["analyses"]:
                analyses.add(Analysis.parse_obj(analysis))
        r = Result(node_bindings=nbindings, analyses=analyses)
        result.update(r)
        return result


class Results(BaseModel):
    """Results."""

    __root__: Optional[HashableSet[Result]]

    class Config:
        title = "results"
        extra = "allow"

    def add(self, result):
        results = self.__root__
        for old_result in results:
            if result == old_result:
                results.remove(result)
                old_result.update(result)
                results.add(old_result)
                return
        results.add(result)

    def __len__(self):
        return len(self.__root__)

    def update(self, other):
        for result in other.__root__:
            self.add(result)

    def parse_obj(obj):
        results = parse_obj_as(Results, obj)
        for result in obj:
            results.add(Result.parse_obj(result))
        return results
