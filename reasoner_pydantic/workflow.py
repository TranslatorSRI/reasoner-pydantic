"""Operations models."""
from enum import Enum
from typing import Any, Optional, Union
from pydantic.class_validators import validator

from pydantic.types import confloat, conint

from .base_model import BaseModel
from .utils import HashableSequence, nonzero_validator


def constant(s: str):
    """Generate a static enum."""
    return Enum(value=s, names={s: s}, type=str)


class RunnerAllowList(BaseModel):
    allowlist: Optional[HashableSequence[str]]
    timeout: Optional[float]
    _nonzero_allowlist = validator("allowlist", allow_reuse=True)(nonzero_validator)

    class Config:
        extra = "forbid"


class RunnerDenyList(BaseModel):
    denylist: Optional[HashableSequence[str]]
    timeout: Optional[float]
    _nonzero_denylist = validator("denylist", allow_reuse=True)(nonzero_validator)

    class Config:
        extra = "forbid"


class RunnerTimeout(BaseModel):
    timeout: Optional[float]

    class Config:
        extra = "forbid"


class RunnerParameters(BaseModel):
    __root__: Optional[Union[RunnerAllowList, RunnerDenyList, RunnerTimeout]]


class BaseOperation(BaseModel):
    runner_parameters: Optional[RunnerParameters]

    class Config:
        extra = "forbid"


class OperationAnnotate(BaseOperation):
    id: constant("annotate")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class AnnotateEdgesParameters(BaseModel):
    attributes: Optional[HashableSequence[str]]


class OperationAnnotateEdges(BaseOperation):
    id: constant("annotate_edges")
    parameters: Optional[AnnotateEdgesParameters]

    class Config:
        extra = "forbid"


class AnnotateNodesParameters(BaseModel):
    attributes: Optional[HashableSequence[str]]


class OperationAnnotateNodes(BaseOperation):
    id: constant("annotate_nodes")
    parameters: Optional[AnnotateNodesParameters]

    class Config:
        extra = "forbid"


class OperationBind(BaseOperation):
    id: constant("bind")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class OperationCompleteResults(BaseOperation):
    id: constant("complete_results")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class EnrichResultsParameters(BaseModel):
    pvalue_threshold: confloat(ge=0.0, le=1.0) = 1e-6
    qnode_keys: Optional[HashableSequence[str]]


class OperationEnrichResults(BaseOperation):
    id: constant("enrich_results")
    parameters: Optional[EnrichResultsParameters]

    class Config:
        extra = "forbid"


class FillAllowParameters(BaseModel):
    allowlist: Optional[HashableSequence[str]]
    qedge_keys: Optional[HashableSequence[str]]
    _nonzero_allowlist = validator("allowlist", allow_reuse=True)(nonzero_validator)

    class Config:
        extra = "forbid"


class FillDenyParameters(BaseModel):
    denylist: Optional[HashableSequence[str]]
    qedge_keys: Optional[HashableSequence[str]]
    _nonzero_denylist = validator("denylist", allow_reuse=True)(nonzero_validator)

    class Config:
        extra = "forbid"


class FillParameters(BaseModel):
    __root__: Union[FillAllowParameters, FillDenyParameters]


class OperationFill(BaseOperation):
    id: constant("fill")
    parameters: Optional[FillParameters]

    class Config:
        extra = "forbid"


class OperationFilterResults(BaseOperation):
    id: constant("filter_results")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class FilterResultsTopNParameters(BaseModel):
    max_results: conint(ge=0)

    class Config:
        extra = "forbid"


class OperationFilterResultsTopN(BaseOperation):
    id: constant("filter_results_top_n")
    parameters: Optional[FilterResultsTopNParameters]

    class Config:
        extra = "forbid"


class OperationFilterKgraph(BaseOperation):
    id: constant("filter_kgraph")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class AboveOrBelowEnum(str, Enum):
    """'above' or 'below'."""

    above = "above"
    below = "below"


class FilterKgraphContinuousKedgeAttributeParameters(BaseModel):
    edge_attribute: str
    threshold: float
    remove_above_or_below: AboveOrBelowEnum
    qedge_keys: Optional[HashableSequence[str]]
    qnode_keys: HashableSequence[str] = []


class OperationFilterKgraphContinuousKedgeAttribute(BaseOperation):
    id: constant("filter_kgraph_continuous_kedge_attribute")
    parameters: FilterKgraphContinuousKedgeAttributeParameters

    class Config:
        extra = "forbid"


class FilterKgraphDiscreteKedgeAttributeParameters(BaseModel):
    edge_attribute: str
    remove_value: Any
    qedge_keys: Optional[HashableSequence[str]]
    qnode_keys: HashableSequence[str] = []


class OperationFilterKgraphDiscreteKedgeAttribute(BaseOperation):
    id: constant("filter_kgraph_discrete_kedge_attribute")
    parameters: FilterKgraphDiscreteKedgeAttributeParameters

    class Config:
        extra = "forbid"


class FilterKgraphDiscreteKnodeAttributeParameters(BaseModel):
    node_attribute: str
    remove_value: Any
    qnode_keys: Optional[HashableSequence[str]]


class OperationFilterKgraphDiscreteKnodeAttribute(BaseOperation):
    id: constant("filter_kgraph_discrete_knode_attribute")
    parameters: FilterKgraphDiscreteKnodeAttributeParameters

    class Config:
        extra = "forbid"


class OperationFilterKgraphOrphans(BaseOperation):
    id: constant("filter_kgraph_orphans")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class TopOrBottomEnum(str, Enum):
    """'top' or 'bottom'."""

    top = "top"
    bottom = "bottom"


class FilterKgraphTopNParameters(BaseModel):
    edge_attribute: str
    max_edges: conint(le=0) = 50
    remove_top_or_bottom: TopOrBottomEnum = TopOrBottomEnum.top
    qedge_keys: Optional[HashableSequence[str]]
    qnode_keys: HashableSequence[str] = []


class FilterKgraphPercentileParameters(BaseModel):
    edge_attribute: str
    threshold: confloat(ge=0, le=100) = 95
    remove_above_or_below: AboveOrBelowEnum = AboveOrBelowEnum.below
    qedge_keys: Optional[HashableSequence[str]]
    qnode_keys: HashableSequence[str] = []


class OperationFilterKgraphPercentile(BaseOperation):
    id: constant("filter_kgraph_percentile")
    parameters: FilterKgraphPercentileParameters

    class Config:
        extra = "forbid"


class PlusOrMinusEnum(str, Enum):
    """'plus' or 'minus'."""

    plus = "plus"
    minus = "minus"


class FilterKgraphStdDevParameters(BaseModel):
    edge_attribute: str
    plus_or_minus_std_dev: PlusOrMinusEnum = PlusOrMinusEnum.plus
    num_sigma: confloat(ge=0) = 1
    remove_above_or_below: AboveOrBelowEnum = AboveOrBelowEnum.below
    qedge_keys: Optional[HashableSequence[str]]
    qnode_keys: HashableSequence[str] = []


class OperationFilterKgraphStdDev(BaseOperation):
    id: constant("filter_kgraph_std_dev")
    parameters: FilterKgraphStdDevParameters

    class Config:
        extra = "forbid"


class OperationFilterKgraphTopN(BaseOperation):
    id: constant("filter_kgraph_top_n")
    parameters: FilterKgraphTopNParameters

    class Config:
        extra = "forbid"


class OperationLookup(BaseOperation):
    id: constant("lookup")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class OperationOverlay(BaseOperation):
    id: constant("overlay")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class OverlayComputeJaccardParameters(BaseModel):
    intermediate_node_key: str
    end_node_keys: HashableSequence[str]
    virtual_relation_label: str


class OperationOverlayComputeJaccard(BaseOperation):
    id: constant("overlay_compute_jaccard")
    parameters: OverlayComputeJaccardParameters

    class Config:
        extra = "forbid"


class OverlayComputeNgdParameters(BaseModel):
    qnode_keys: HashableSequence[str]
    virtual_relation_label: str


class OperationOverlayComputeNgd(BaseOperation):
    id: constant("overlay_compute_ngd")
    parameters: OverlayComputeNgdParameters

    class Config:
        extra = "forbid"


class OperationOverlayConnectKnodes(BaseOperation):
    id: constant("overlay_connect_knodes")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class OverlayFisherExactTestParameters(BaseModel):
    subject_qnode_key: str
    object_qnode_key: str
    virtual_relation_label: str
    rel_edge_key: Optional[str]


class OperationOverlayFisherExactTest(BaseOperation):
    id: constant("overlay_fisher_exact_test")
    parameters: OverlayFisherExactTestParameters

    class Config:
        extra = "forbid"


class OperationRestate(BaseOperation):
    id: constant("restate")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class OperationScore(BaseOperation):
    id: constant("score")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class OperationSortResults(BaseOperation):
    id: constant("sort_results")
    parameters: Optional[Any]

    class Config:
        extra = "forbid"


class AscOrDescEnum(str, Enum):
    """'ascending' or 'descending'."""

    ascending = "ascending"
    descending = "descending"


class SortResultsEdgeAttributeParameters(BaseModel):
    edge_attribute: str
    ascending_or_descending: AscOrDescEnum
    qedge_keys: Optional[HashableSequence[str]]


class OperationSortResultsEdgeAttribute(BaseOperation):
    id: constant("sort_results_edge_attribute")
    parameters: SortResultsEdgeAttributeParameters

    class Config:
        extra = "forbid"


class SortResultsNodeAttributeParameters(BaseModel):
    node_attribute: str
    ascending_or_descending: AscOrDescEnum
    qnode_keys: Optional[HashableSequence[str]]


class OperationSortResultsNodeAttribute(BaseOperation):
    id: constant("sort_results_node_attribute")
    parameters: SortResultsNodeAttributeParameters

    class Config:
        extra = "forbid"


class SortResultsScoreParameters(BaseModel):
    ascending_or_descending: AscOrDescEnum


class OperationSortResultsScore(BaseOperation):
    id: constant("sort_results_score")
    parameters: SortResultsScoreParameters

    class Config:
        extra = "forbid"


operations = [
    OperationAnnotate,
    OperationAnnotateEdges,
    OperationAnnotateNodes,
    OperationBind,
    OperationCompleteResults,
    OperationEnrichResults,
    OperationFill,
    OperationFilterKgraph,
    OperationFilterKgraphContinuousKedgeAttribute,
    OperationFilterKgraphDiscreteKedgeAttribute,
    OperationFilterKgraphDiscreteKnodeAttribute,
    OperationFilterKgraphOrphans,
    OperationFilterKgraphPercentile,
    OperationFilterKgraphStdDev,
    OperationFilterKgraphTopN,
    OperationFilterResults,
    OperationFilterResultsTopN,
    OperationLookup,
    OperationOverlay,
    OperationOverlayComputeJaccard,
    OperationOverlayComputeNgd,
    OperationOverlayConnectKnodes,
    OperationOverlayFisherExactTest,
    OperationRestate,
    OperationScore,
    OperationSortResults,
    OperationSortResultsEdgeAttribute,
    OperationSortResultsNodeAttribute,
    OperationSortResultsScore,
]


class Operation(BaseModel):
    __root__: Union[
        OperationAnnotate,
        OperationAnnotateEdges,
        OperationAnnotateNodes,
        OperationBind,
        OperationCompleteResults,
        OperationEnrichResults,
        OperationFill,
        OperationFilterKgraph,
        OperationFilterKgraphContinuousKedgeAttribute,
        OperationFilterKgraphDiscreteKedgeAttribute,
        OperationFilterKgraphDiscreteKnodeAttribute,
        OperationFilterKgraphOrphans,
        OperationFilterKgraphPercentile,
        OperationFilterKgraphStdDev,
        OperationFilterKgraphTopN,
        OperationFilterResults,
        OperationFilterResultsTopN,
        OperationLookup,
        OperationOverlay,
        OperationOverlayComputeJaccard,
        OperationOverlayComputeNgd,
        OperationOverlayConnectKnodes,
        OperationOverlayFisherExactTest,
        OperationRestate,
        OperationScore,
        OperationSortResults,
        OperationSortResultsEdgeAttribute,
        OperationSortResultsNodeAttribute,
        OperationSortResultsScore,
    ]


class Workflow(BaseModel):
    __root__: HashableSequence[Operation]
