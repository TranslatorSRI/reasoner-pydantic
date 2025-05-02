from pydantic import AfterValidator, ConfigDict
from reasoner_pydantic.shared import CURIE, KnowledgeType
from typing import Annotated, Optional

from reasoner_pydantic import BiolinkEntity, BiolinkPredicate

from .base_model import BaseModel
from .utils import HashableMapping, HashableSequence, nonzero_validator


class MetaAttribute(BaseModel):
    """MetaAttribute."""

    attribute_type_id: CURIE
    attribute_source: Optional[str] = None
    original_attribute_names: Optional[HashableSequence[str]] = None
    constraint_use: Optional[bool] = False
    constraint_name: Optional[str] = None


class MetaNode(BaseModel):
    id_prefixes: Annotated[HashableSequence[str], AfterValidator(nonzero_validator)]
    attributes: Optional[HashableSequence[MetaAttribute]] = None
    model_config = ConfigDict(extra="forbid")


class MetaQualifier(BaseModel):
    qualifier_type_id: CURIE
    applicable_values: Optional[HashableSequence[str]] = None


class MetaEdge(BaseModel):
    subject: BiolinkEntity
    predicate: BiolinkPredicate
    object: BiolinkEntity
    qualifiers: Optional[HashableSequence[MetaQualifier]] = None
    attributes: Optional[HashableSequence[MetaAttribute]] = None
    knowledge_types: Optional[HashableSequence[KnowledgeType]] = None
    association: Optional[BiolinkEntity] = None
    model_config = ConfigDict(extra="forbid")


class MetaKnowledgeGraph(BaseModel):
    nodes: HashableMapping[str, MetaNode]
    edges: HashableSequence[MetaEdge]
