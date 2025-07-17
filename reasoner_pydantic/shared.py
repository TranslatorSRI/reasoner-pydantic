"""Shared models."""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Annotated, Hashable, Optional

from pydantic import BeforeValidator, ConfigDict, Field
from pydantic.types import StringConstraints

from .base_model import BaseModel
from .utils import HashableSequence, make_hashable


# TODO: potential add validation for structure of CURIE
CURIE = str


class ResourceRoleEnum(str, Enum):
    """Types of resources"""

    aggregator_knowledge_source = "aggregator_knowledge_source"
    primary_knowledge_source = "primary_knowledge_source"
    supporting_data_source = "supporting_data_source"


class KnowledgeType(str, Enum):
    "Knowledge Type."

    lookup = "lookup"
    inferred = "inferred"


EdgeIdentifier = str


class Attribute(BaseModel):
    """Node/edge attribute."""

    attribute_type_id: Annotated[CURIE, Field(title="type")]
    value: Annotated[Hashable, BeforeValidator(make_hashable)]
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
