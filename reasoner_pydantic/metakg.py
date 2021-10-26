from reasoner_pydantic.shared import CURIE
from typing import Optional

from pydantic import conlist
from reasoner_pydantic import BiolinkEntity, BiolinkPredicate

from .base_model import BaseModel
from .utils import HashableMapping, HashableSequence

class MetaAttribute(BaseModel):
    """MetaAttribute."""
    attribute_type_id: CURIE
    attribute_source: Optional[str]
    original_attribute_names: Optional[HashableSequence[str]]
    constraint_use: Optional[bool] = False
    constraint_name: Optional[str]


class MetaNode(BaseModel):
    id_prefixes: conlist(str, min_items=1)
    attributes: Optional[HashableSequence[MetaAttribute]]

    class Config:
        extra = 'forbid'


class MetaEdge(BaseModel):
    subject: BiolinkEntity
    predicate: BiolinkPredicate
    object: BiolinkEntity
    attributes: Optional[HashableSequence[MetaAttribute]]

    class Config:
        extra = 'forbid'


class MetaKnowledgeGraph(BaseModel):
    nodes: HashableMapping[str, MetaNode]
    edges: HashableSequence[MetaEdge]
