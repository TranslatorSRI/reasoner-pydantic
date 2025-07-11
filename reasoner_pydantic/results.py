"""Results models."""

import copy
from typing import Optional, Union

from pydantic import Field, parse_obj_as, ValidationError

from .base_model import BaseModel
from .utils import HashableMapping, HashableSet, HashableSequence
from .shared import Attribute, CURIE


class EdgeBinding(BaseModel):
    """Edge binding."""

    id: str = Field(..., title="knowledge graph id", nullable=False)

    attributes: HashableSet[Attribute] = Field(..., nullable=False)

    class Config:
        title = "edge binding"
        schema_extra = {
            "example": {
                "id": "string",
            },
        }
        extra = "allow"


class PathBinding(BaseModel):
    """Path binding."""

    id: str = Field(..., title="auxiliary graph id", nullable=False)

    class Config:
        title = "path binding"
        schema_extra = {
            "example": {
                "id": "string",
            },
        }
        extra = "allow"


class BaseAnalysis(BaseModel):
    """Base Analysis."""

    resource_id: CURIE = Field(
        ...,
        title="resource infores",
    )

    score: Optional[float] = Field(
        None,
        format="float",
    )

    support_graphs: Optional[HashableSet[str]] = Field(None, nullable=True)

    scoring_method: Optional[str] = Field(None, nullable=True)

    attributes: Optional[HashableSet[Attribute]] = Field(None, nullable=True)


class Analysis(BaseAnalysis):
    """Standard analysis"""

    edge_bindings: HashableMapping[str, HashableSet[EdgeBinding]] = Field(
        ...,
        title="list of edge bindings",
    )

    class Config:
        title = "standard analysis"
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
        for k in other.edge_bindings:
            if k in self.edge_bindings:
                self.edge_bindings[k].update(copy.deepcopy(other.edge_bindings[k]))
            else:
                self.edge_bindings[k] = copy.deepcopy(other.edge_bindings[k])
        if other.attributes:
            if self.attributes:
                self.attributes.update(other.attributes)
            else:
                self.attributes = other.attributes
        if other.support_graphs:
            if self.support_graphs:
                self.support_graphs.update(other.support_graphs)
            else:
                self.support_graphs = other.support_graphs


class PathfinderAnalysis(BaseAnalysis):
    """Pathfinder Analysis."""

    path_bindings: HashableMapping[str, HashableSet[PathBinding]] = Field(
        ...,
        title="list of path bindings",
    )

    class Config:
        title = "pathfinder analysis"
        extra = "allow"

    def __hash__(self) -> int:
        return hash(
            (
                self.resource_id,
                self.path_bindings,
                self.score,
                self.support_graphs,
                self.scoring_method,
            )
        )

    def update(self, other):
        for k in other.path_bindings:
            if k in self.path_bindings:
                self.path_bindings[k].update(copy.deepcopy(other.path_bindings[k]))
            else:
                self.path_bindings[k] = copy.deepcopy(other.path_bindings[k])
        if other.attributes:
            if self.attributes:
                self.attributes.update(other.attributes)
            else:
                self.attributes = other.attributes
        if other.support_graphs:
            if self.support_graphs:
                self.support_graphs.update(other.support_graphs)
            else:
                self.support_graphs = other.support_graphs


class NodeBinding(BaseModel):
    """Node binding."""

    id: CURIE = Field(..., title="knowledge graph id", nullable=False)

    query_id: Optional[CURIE] = Field(None, title="query graph id")

    attributes: HashableSet[Attribute] = Field(..., nullable=False)

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
        ..., title="list of node bindings", nullable=False
    )

    analyses: Union[HashableSet[Analysis], HashableSet[PathfinderAnalysis]] = Field(
        ..., title="list of anlysis blocks", nullable=False
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
        if "analyses" in obj.keys() and len(obj["analyses"]):
            if "edge_bindings" in obj["analyses"][0].keys():
                analyses = HashableSet[Analysis]()
                for analysis in obj["analyses"]:
                    analyses.add(Analysis.parse_obj(analysis))
            elif "path_bindings" in obj["analyses"][0].keys():
                analyses = HashableSet[PathfinderAnalysis]()
                for analysis in obj["analyses"]:
                    analyses.add(PathfinderAnalysis.parse_obj(analysis))
            else:
                raise ValidationError(["Analyses missing bindings"], Result)
        else:
            analyses = []
        r = Result(node_bindings=nbindings, analyses=analyses)
        result.update(r)
        return result

    def combine_analyses_by_resource_id(self):
        # Useful when a service unintentionally adds multiple analyses to a single result
        # Combines all of those analyses
        combine = HashableMapping[str, Analysis]()
        analyses = HashableSequence.parse_obj([analysis for analysis in self.analyses])
        for i, analysis in enumerate(analyses):
            if analysis.resource_id not in combine:
                combine[analysis.resource_id] = analysis
            for j, analysis_to_compare in enumerate(analyses[i + 1 :]):
                if (
                    analysis.resource_id == analysis_to_compare.resource_id
                    and analysis != analysis_to_compare
                ):
                    combine[analysis.resource_id].update(analysis_to_compare)

        combined_analyses = HashableSet[Analysis]()
        for analysis in combine.values():
            combined_analyses.add(analysis)

        self.analyses = combined_analyses


class Results(BaseModel):
    """Results."""

    __root__: Optional[HashableSequence[Result]]

    class Config:
        title = "results"
        extra = "allow"

    def append(self, result):
        self.__root__.append(result)

    def add(self, result):
        results = self.__root__
        try:
            # this is slow for larger results
            results[results.index(result)].update(result)
        except ValueError:
            results.append(result)

    def __len__(self):
        return len(self.__root__)

    def __iter__(self):
        return self.__root__.__iter__()

    def __contains__(self, v):
        return self.__root__.__contains__(v)

    def __getitem__(self, i):
        return self.__root__.__getitem__(i)

    def update(self, other):
        results = parse_obj_as(HashableMapping, {})
        for result in other:
            if not isinstance(result, Result):
                result = Result.parse_obj(result)
            result_hash = hash(result)
            if result_hash in results:
                results[result_hash].update(result)
            else:
                results[hash(result)] = result

    def parse_obj(obj):
        parse_obj_as(Results, obj)
        results = parse_obj_as(HashableMapping, {})
        for result in obj:
            result = Result.parse_obj(result)
            result_hash = hash(result)
            if result_hash in results:
                results[result_hash].update(result)
            else:
                results[hash(result)] = result
        return parse_obj_as(Results, list(results.values()))
