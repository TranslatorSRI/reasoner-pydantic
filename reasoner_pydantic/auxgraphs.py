"""Auxiliary Graphs model"""

from typing import Annotated, Any
from pydantic import ConfigDict, Field

from .base_model import BaseModel
from .utils import HashableMapping, HashableSet
from .shared import Attribute, EdgeIdentifier


class AuxiliaryGraph(BaseModel):
    """Auxiliary Graph"""

    edges: Annotated[
        HashableSet[EdgeIdentifier], Field(title="edges in auxiliary graph")
    ]

    attributes: HashableSet[Attribute]
    model_config = ConfigDict(title="auxiliary graph", extra="allow")


class AuxiliaryGraphs(HashableMapping[str, AuxiliaryGraph]):
    """Auxiliary Graphs"""

    model_config = ConfigDict(title="auxiliary graphs")

    def update(self, other: object, *_args: Any, **_kwargs: Any):
        if not isinstance(other, HashableMapping):
            raise TypeError("AuxiliaryGraphs may only be updated with AuxiliaryGraphs.")
        self.root.update(other.root)

    def values(self):
        return self.root.values()

    def items(self):
        return self.root.items()

    def keys(self):
        return self.root.keys()

    def __setitem__(self, k: str, v: AuxiliaryGraph):
        self.root[k] = v

    def __getitem__(self, k: str):
        return self.root[k]

    def __iter__(self):
        return iter(self.root)
