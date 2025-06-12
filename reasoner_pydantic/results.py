"""Results models."""

import copy
from typing import Annotated, Optional, Union

from pydantic import ConfigDict, Field, model_validator

from .base_model import BaseModel
from .utils import HashableMapping, HashableSet, HashableSequence 
from .shared import Attribute, CURIE, EdgeIdentifier


class EdgeBinding(BaseModel):
    """Edge binding."""

    id: Annotated[EdgeIdentifier, Field(title="knowledge graph id")]
    attributes: HashableSet[Attribute]

    model_config = ConfigDict(
        title="edge binding",
        json_schema_extra={
            "example": {
                "id": "string",
            },
        },
        extra="allow",
    )


class PathBinding(BaseModel):
    """Path binding."""

    id: Annotated[str, Field(title="auxiliary graph id")]

    model_config = ConfigDict(
        title="path binding",
        json_schema_extra={ "example": {"id": "string"} }
        extra="allow"
    )


class BaseAnalysis(BaseModel):
    """Base Analysis."""

    resource_id: Annotated[
        CURIE,
        Field(
            title="resource infores",
        ),
    ]

    edge_bindings: Annotated[
        HashableMapping[str, HashableSet[EdgeBinding]],
        Field(
            title="list of edge bindings",
        ),
    ]
    score: Optional[float] = None
    support_graphs: Optional[HashableSet[str]] = None
    scoring_method: Optional[str] = None
    attributes: Optional[HashableSet[Attribute]] = None


class Analysis(BaseAnalysis):
    """Standard analysis"""

    edge_bindings: Annotated[
        HashableMapping[str, HashableSet[EdgeBinding]],
        Field(
            title="list of edge bindings",
        ),
    ]

    model_config = ConfigDict(title="standard analysis", extra="allow")

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

    def update(self, other: object):
        if not isinstance(other, Analysis):
            raise TypeError("Analysis may only be updated with another Analysis.")
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

    path_bindings: Annotated[
        HashableMapping[str, HashableSet[PathBinding]],
        Field(
            title="list of path bindings",
        )
    ]

    model_config = ConfigDict(title="pathfinder analysis", extra="allow")

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

    id: Annotated[
        CURIE,
        Field(
            title="knowledge graph id",
        ),
    ]
    query_id: Annotated[Optional[CURIE], Field(title="query graph id")] = None
    attributes: HashableSet[Attribute]

    model_config = ConfigDict(
        title="node binding",
        json_schema_extra={
            "example": {
                "id": "x:string",
            },
        },
        extra="allow",
    )


class Result(BaseModel):
    """Result."""

    node_bindings: Annotated[
        HashableMapping[str, HashableSet[NodeBinding]],
        Field(
            title="list of node bindings",
        ),
    ]
    analyses: Annotated[
        Union[HashableSet[Analysis], HashableSet[PathfinderAnalysis]],
        Field(
            title="list of anlysis blocks",
        ),
    ]

    model_config = ConfigDict(title="result", extra="allow")

    def update(self, other: object):
        if not isinstance(other, Result):
            raise TypeError("Result may only be updated with another Result.")
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

    def combine_analyses_by_resource_id(self):
        # Useful when a service unintentionally adds multiple analyses to a single result
        # Combines all of those analyses
        combine = HashableMapping[CURIE, Analysis]()
        analyses = HashableSequence[Analysis]([analysis for analysis in self.analyses])
        for _ in range(len(analyses)):
            analysis = analyses.pop()
            if analysis.resource_id not in combine:
                combine[analysis.resource_id] = analysis
            for analysis_to_compare in analyses:
                if (
                    analysis.resource_id == analysis_to_compare.resource_id
                    and analysis != analysis_to_compare
                ):
                    combine[analysis.resource_id].update(analysis_to_compare)

        combined_analyses = HashableSet[Analysis]()
        for analysis in combine.values():
            combined_analyses.add(analysis)

        self.analyses = combined_analyses


class Results(HashableSequence[Result]):
    """Results."""

    model_config = ConfigDict(title="allow")

    def append(self, value: Result):
        self.root.append(value)

    def add(self, result: Result):
        results = self.root
        try:
            # this is slow for larger results
            results[results.index(result)].update(result)
        except ValueError:
            results.append(result)

    def __len__(self):
        return len(self.root)

    def __iter__(self):
        return self.root.__iter__()

    def __contains__(self, v):
        return self.root.__contains__(v)

    def __getitem__(self, i):
        return self.root.__getitem__(i)

    def update(self, other: object):
        results = HashableMapping[int, Result](
            {hash(result): result for result in self.root}
        )
        for result in other:
            if not isinstance(result, Result):
                result = Result.model_validate(result)
            result_hash = hash(result)
            if result_hash in results:
                results[result_hash].update(result)
            else:
                results[hash(result)] = result
        self.root.clear()
        self.root.extend(results.values())

    @model_validator(mode="after")
    def merge_results(self):
        results: dict[int, Result] = {}
        for result in self.root:
            result_hash = hash(result)
            if result_hash in results:
                results[result_hash].update(result)
            else:
                results[result_hash] = result

        self.root.clear()
        self.root.extend(results.values())
        return self
