from pydantic import validator
from reasoner_pydantic.shared import CURIE, KnowledgeType
from typing import Optional

from reasoner_pydantic import BiolinkEntity, BiolinkPredicate, BiolinkQualifier

from .base_model import BaseModel
from .utils import HashableMapping, HashableSequence, nonzero_validator


class MetaAttribute(BaseModel):
    """MetaAttribute."""

    attribute_type_id: CURIE
    attribute_source: Optional[str]
    original_attribute_names: Optional[HashableSequence[str]]
    constraint_use: Optional[bool] = False
    constraint_name: Optional[str]


class MetaNode(BaseModel):
    id_prefixes: HashableSequence[str]
    _nonzero_id_prefixes = validator("id_prefixes", allow_reuse=True)(nonzero_validator)
    attributes: Optional[HashableSequence[MetaAttribute]]

    class Config:
        extra = "forbid"


class MetaQualifier(BaseModel):
    qualifier_type_id: CURIE
    applicable_values: Optional[HashableSequence[str]]


class MetaEdge(BaseModel):
    subject: BiolinkEntity
    predicate: BiolinkPredicate
    object: BiolinkEntity
    qualifiers: Optional[HashableSequence[MetaQualifier]]
    attributes: Optional[HashableSequence[MetaAttribute]]
    knowledge_types: Optional[HashableSequence[KnowledgeType]]
    association: Optional[BiolinkEntity]

    class Config:
        extra = "forbid"


class MetaKnowledgeGraph(BaseModel):
    nodes: HashableMapping[str, MetaNode]
    edges: HashableSequence[MetaEdge]
