from typing import Dict, List, Optional

from pydantic import BaseModel, conlist
from reasoner_pydantic import BiolinkEntity, BiolinkPredicate


class MetaNode(BaseModel):
    id_prefixes: conlist(str, min_items=1)

    class Config:
        extra = 'forbid'


class MetaEdge(BaseModel):
    subject: BiolinkEntity
    predicate: BiolinkPredicate
    object: BiolinkEntity
    relations: Optional[List[str]]

    class Config:
        extra = 'forbid'


class MetaKnowledgeGraph(BaseModel):
    nodes: Optional[Dict[str, MetaNode]]
    edges: Optional[conlist(MetaEdge, min_items=1)]
