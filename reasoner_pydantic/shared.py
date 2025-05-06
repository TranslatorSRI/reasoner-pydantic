"""Shared models."""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional

from pydantic import ConfigDict, Field
from pydantic.types import StringConstraints

from .base_model import BaseModel, RootModel
from .utils import HashableSequence, stable_hash


class StrValue(RootModel[str]):
    """Generic handling for string values that supports equality with normal strings."""

    root: str

    def __eq__(self, other: object) -> bool:
        return self.root == other.__str__()

    def __hash__(self) -> int:
        return stable_hash(self.root)

    def __str__(self) -> str:
        return self.root

    def __json__(self) -> str:
        return self.root


# TODO: potential add validation for structure of CURIE
class CURIE(StrValue):
    """Compact URI."""


class ResourceRoleEnum(str, Enum):
    """Types of resources"""

    aggregator_knowledge_source = "aggregator_knowledge_source"
    primary_knowledge_source = "primary_knowledge_source"
    supporting_data_source = "supporting_data_source"


class KnowledgeType(str, Enum):
    "Knowledge Type."

    lookup = "lookup"
    inferred = "inferred"


class EdgeIdentifier(StrValue):
    """Identifier for an edge in a knowledge graph"""


class Attribute(BaseModel):
    """Node/edge attribute."""

    attribute_type_id: Annotated[CURIE, Field(title="type")]
    value: Any
    value_type_id: Optional[CURIE] = None
    original_attribute_name: Optional[str] = None
    value_url: Optional[str] = None
    attribute_source: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[HashableSequence["Attribute"]] = None
    model_config = ConfigDict(extra="forbid")


BiolinkQualifier = Annotated[
    str, StringConstraints(pattern=re.compile("^biolink:[a-z][a-z_]*$"))
]


class Qualifier(BaseModel):
    """Edge qualifier."""

    qualifier_type_id: Annotated[BiolinkQualifier, Field(title="type")]

    qualifier_value: Annotated[str, Field(title="value")]


BiolinkPredicate = Annotated[
    str, StringConstraints(pattern=re.compile("^biolink:[a-z][a-z_]*$"))
]
BiolinkEntity = Annotated[
    str, StringConstraints(pattern=re.compile("^biolink:[A-Z][a-zA-Z_]*$"))
]


class LogLevel(str, Enum):
    """Log level."""

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class LogEntry(BaseModel):
    """Log entry."""

    timestamp: Optional[datetime] = None
    level: Optional[LogLevel] = None
    code: Optional[str] = None
    message: str = ""
    model_config = ConfigDict(extra="allow")
