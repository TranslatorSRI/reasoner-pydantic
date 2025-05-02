"""Operations models."""

from enum import Enum
from typing import Any, Literal, Optional, Union


from .base_model import BaseModel, RootModel
from .utils import HashableSequence
from .shared import BiolinkPredicate
from pydantic import Field, ConfigDict
from typing import Annotated


class RunnerAllowList(BaseModel):
    allowlist: Optional[HashableSequence[str]] = None
    timeout: Optional[float] = None
    model_config = ConfigDict(extra="forbid")


class RunnerDenyList(BaseModel):
    denylist: Optional[HashableSequence[str]] = None
    timeout: Optional[float] = None
    model_config = ConfigDict(extra="forbid")


class RunnerTimeout(BaseModel):
    timeout: Optional[float] = None
    model_config = ConfigDict(extra="forbid")


RunnerParameters = RootModel[
    Optional[Union[RunnerAllowList, RunnerDenyList, RunnerTimeout]]
]


class BaseOperation(BaseModel):
    runner_parameters: Optional[RunnerParameters] = None
    model_config = ConfigDict(extra="forbid")


class OperationAnnotate(BaseOperation):
    id: Literal["annotate"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class AnnotateEdgesParameters(BaseModel):
    attributes: Optional[HashableSequence[str]] = None


class OperationAnnotateEdges(BaseOperation):
    id: Literal["annotate_edges"]
    parameters: Optional[AnnotateEdgesParameters] = None
    model_config = ConfigDict(extra="forbid")


class AnnotateNodesParameters(BaseModel):
    attributes: Optional[HashableSequence[str]] = None


class OperationAnnotateNodes(BaseOperation):
    id: Literal["annotate_nodes"]
    parameters: Optional[AnnotateNodesParameters] = None
    model_config = ConfigDict(extra="forbid")


class OperationBind(BaseOperation):
    id: Literal["bind"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class OperationCompleteResults(BaseOperation):
    id: Literal["complete_results"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class EnrichResultsParameters(BaseModel):
    pvalue_threshold: Annotated[float, Field(ge=0.0, le=1.0)] = 1e-6
    qnode_keys: Optional[HashableSequence[str]] = None
    predicates_to_exclude: Optional[HashableSequence[BiolinkPredicate]] = None


class OperationEnrichResults(BaseOperation):
    id: Literal["enrich_results"]
    parameters: Optional[EnrichResultsParameters] = None
    model_config = ConfigDict(extra="forbid")


class FillAllowParameters(BaseModel):
    allowlist: Optional[HashableSequence[str]] = None
    qedge_keys: Optional[HashableSequence[str]] = None
    model_config = ConfigDict(extra="forbid")


class FillDenyParameters(BaseModel):
    denylist: Optional[HashableSequence[str]] = None
    qedge_keys: Optional[HashableSequence[str]] = None
    model_config = ConfigDict(extra="forbid")


FillParameters = RootModel[Union[FillAllowParameters, FillDenyParameters]]


class OperationFill(BaseOperation):
    id: Literal["fill"]
    parameters: Optional[FillParameters] = None
    model_config = ConfigDict(extra="forbid")


class OperationFilterResults(BaseOperation):
    id: Literal["filter_results"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class FilterResultsTopNParameters(BaseModel):
    max_results: Annotated[int, Field(ge=0)]
    model_config = ConfigDict(extra="forbid")


class OperationFilterResultsTopN(BaseOperation):
    id: Literal["filter_results_top_n"]
    parameters: Optional[FilterResultsTopNParameters] = None
    model_config = ConfigDict(extra="forbid")


class OperationFilterKgraph(BaseOperation):
    id: Literal["filter_kgraph"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class AboveOrBelowEnum(str, Enum):
    """'above' or 'below'."""

    above = "above"
    below = "below"


class FilterKgraphContinuousKedgeAttributeParameters(BaseModel):
    edge_attribute: str
    threshold: float
    remove_above_or_below: AboveOrBelowEnum
    qedge_keys: Optional[HashableSequence[str]] = None
    qnode_keys: HashableSequence[str] = Field(
        default_factory=lambda: HashableSequence[str]()
    )


class OperationFilterKgraphContinuousKedgeAttribute(BaseOperation):
    id: Literal["filter_kgraph_continuous_kedge_attribute"]
    parameters: FilterKgraphContinuousKedgeAttributeParameters
    model_config = ConfigDict(extra="forbid")


class FilterKgraphDiscreteKedgeAttributeParameters(BaseModel):
    edge_attribute: str
    remove_value: Any = None
    qedge_keys: Optional[HashableSequence[str]] = None
    qnode_keys: HashableSequence[str] = Field(
        default_factory=lambda: HashableSequence[str]()
    )


class OperationFilterKgraphDiscreteKedgeAttribute(BaseOperation):
    id: Literal["filter_kgraph_discrete_kedge_attribute"]
    parameters: FilterKgraphDiscreteKedgeAttributeParameters
    model_config = ConfigDict(extra="forbid")


class FilterKgraphDiscreteKnodeAttributeParameters(BaseModel):
    node_attribute: str
    remove_value: Any = None
    qnode_keys: Optional[HashableSequence[str]] = None


class OperationFilterKgraphDiscreteKnodeAttribute(BaseOperation):
    id: Literal["filter_kgraph_discrete_knode_attribute"]
    parameters: FilterKgraphDiscreteKnodeAttributeParameters
    model_config = ConfigDict(extra="forbid")


class OperationFilterKgraphOrphans(BaseOperation):
    id: Literal["filter_kgraph_orphans"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class TopOrBottomEnum(str, Enum):
    """'top' or 'bottom'."""

    top = "top"
    bottom = "bottom"


class FilterKgraphTopNParameters(BaseModel):
    edge_attribute: str
    max_edges: Annotated[int, Field(le=0)] = 50
    remove_top_or_bottom: TopOrBottomEnum = TopOrBottomEnum.top
    qedge_keys: Optional[HashableSequence[str]] = None
    qnode_keys: HashableSequence[str] = Field(
        default_factory=lambda: HashableSequence[str]()
    )


class FilterKgraphPercentileParameters(BaseModel):
    edge_attribute: str
    threshold: Annotated[float, Field(ge=0, le=100)] = 95
    remove_above_or_below: AboveOrBelowEnum = AboveOrBelowEnum.below
    qedge_keys: Optional[HashableSequence[str]] = None
    qnode_keys: HashableSequence[str] = Field(
        default_factory=lambda: HashableSequence[str]()
    )


class OperationFilterKgraphPercentile(BaseOperation):
    id: Literal["filter_kgraph_percentile"]
    parameters: FilterKgraphPercentileParameters
    model_config = ConfigDict(extra="forbid")


class PlusOrMinusEnum(str, Enum):
    """'plus' or 'minus'."""

    plus = "plus"
    minus = "minus"


class FilterKgraphStdDevParameters(BaseModel):
    edge_attribute: str
    plus_or_minus_std_dev: PlusOrMinusEnum = PlusOrMinusEnum.plus
    num_sigma: Annotated[float, Field(ge=0)] = 1
    remove_above_or_below: AboveOrBelowEnum = AboveOrBelowEnum.below
    qedge_keys: Optional[HashableSequence[str]] = None
    qnode_keys: HashableSequence[str] = Field(
        default_factory=lambda: HashableSequence[str]()
    )


class OperationFilterKgraphStdDev(BaseOperation):
    id: Literal["filter_kgraph_std_dev"]
    parameters: FilterKgraphStdDevParameters
    model_config = ConfigDict(extra="forbid")


class OperationFilterKgraphTopN(BaseOperation):
    id: Literal["filter_kgraph_top_n"]
    parameters: FilterKgraphTopNParameters
    model_config = ConfigDict(extra="forbid")


class OperationLookup(BaseOperation):
    id: Literal["lookup"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class OperationLookupAndScore(BaseOperation):
    id: Literal["lookup_and_score"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class OperationOverlay(BaseOperation):
    id: Literal["overlay"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class OverlayComputeJaccardParameters(BaseModel):
    intermediate_node_key: str
    end_node_keys: HashableSequence[str]
    virtual_relation_label: str


class OperationOverlayComputeJaccard(BaseOperation):
    id: Literal["overlay_compute_jaccard"]
    parameters: OverlayComputeJaccardParameters
    model_config = ConfigDict(extra="forbid")


class OverlayComputeNgdParameters(BaseModel):
    qnode_keys: HashableSequence[str]
    virtual_relation_label: str


class OperationOverlayComputeNgd(BaseOperation):
    id: Literal["overlay_compute_ngd"]
    parameters: OverlayComputeNgdParameters
    model_config = ConfigDict(extra="forbid")


class OperationOverlayConnectKnodes(BaseOperation):
    id: Literal["overlay_connect_knodes"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class OverlayFisherExactTestParameters(BaseModel):
    subject_qnode_key: str
    object_qnode_key: str
    virtual_relation_label: str
    rel_edge_key: Optional[str] = None


class OperationOverlayFisherExactTest(BaseOperation):
    id: Literal["overlay_fisher_exact_test"]
    parameters: OverlayFisherExactTestParameters
    model_config = ConfigDict(extra="forbid")


class OperationRestate(BaseOperation):
    id: Literal["restate"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class OperationScore(BaseOperation):
    id: Literal["score"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class OperationSortResults(BaseOperation):
    id: Literal["sort_results"]
    parameters: Optional[Any] = None
    model_config = ConfigDict(extra="forbid")


class AscOrDescEnum(str, Enum):
    """'ascending' or 'descending'."""

    ascending = "ascending"
    descending = "descending"


class SortResultsEdgeAttributeParameters(BaseModel):
    edge_attribute: str
    ascending_or_descending: AscOrDescEnum
    qedge_keys: Optional[HashableSequence[str]] = None


class OperationSortResultsEdgeAttribute(BaseOperation):
    id: Literal["sort_results_edge_attribute"]
    parameters: SortResultsEdgeAttributeParameters
    model_config = ConfigDict(extra="forbid")


class SortResultsNodeAttributeParameters(BaseModel):
    node_attribute: str
    ascending_or_descending: AscOrDescEnum
    qnode_keys: Optional[HashableSequence[str]] = None


class OperationSortResultsNodeAttribute(BaseOperation):
    id: Literal["sort_results_node_attribute"]
    parameters: SortResultsNodeAttributeParameters
    model_config = ConfigDict(extra="forbid")


class SortResultsScoreParameters(BaseModel):
    ascending_or_descending: AscOrDescEnum


class OperationSortResultsScore(BaseOperation):
    id: Literal["sort_results_score"]
    parameters: SortResultsScoreParameters
    model_config = ConfigDict(extra="forbid")


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
    OperationLookupAndScore,
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

Operation = RootModel[
    Union[
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
        OperationLookupAndScore,
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
]


Workflow = HashableSequence[Operation]
