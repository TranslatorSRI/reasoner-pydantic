from reasoner_pydantic.shared import CURIE
from typing import Dict, List, Optional

from pydantic import BaseModel, conlist
from reasoner_pydantic import BiolinkEntity, BiolinkPredicate


class MetaAttribute(BaseModel):
    """MetaAttribute."""
    attribute_type_id: CURIE
    attribute_source: Optional[str]
    original_attribute_names: Optional[List[str]]
    constraint_use: Optional[bool] = False
    constraint_name: Optional[str]


class MetaNode(BaseModel):
    id_prefixes: conlist(str, min_items=1)
    attributes: Optional[List[MetaAttribute]]

    class Config:
        extra = 'forbid'


class MetaEdge(BaseModel):
    subject: BiolinkEntity
    predicate: BiolinkPredicate
    object: BiolinkEntity
    attributes: Optional[List[MetaAttribute]]

    class Config:
        extra = 'forbid'


class MetaKnowledgeGraph(BaseModel):
    nodes: Dict[str, MetaNode]
    edges: List[MetaEdge]
