"""Shared models."""
from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
import string
from typing import Any, Optional

from pydantic import Field
from pydantic.types import ConstrainedStr

from .base_model import BaseModel
from .utils import HashableSequence


# TODO: potential add validation for structure of CURIE
class CURIE(str):
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


class EdgeIdentifier(str):
    """Identifier for an edge in a knowledge graph"""


class RecursiveAttribute(BaseModel):
    """Attribute subattribute."""

    attribute_type_id: CURIE = Field(..., title="type")
    value: Any = Field(..., title="value")
    value_type_id: Optional[CURIE] = Field(
        None,
        title="value_type_id",
        nullable=True,
    )
    original_attribute_name: Optional[str] = Field(None, nullable=True)
    value_url: Optional[str] = Field(None, nullable=True)
    attribute_source: Optional[str] = Field(None, nullable=True)
    description: Optional[str] = Field(None, nullable=True)
    attributes: Optional[HashableSequence[RecursiveAttribute]] = Field(
        None, nullable=True
    )

    class Config:
        extra = "forbid"


class SubAttribute(BaseModel):
    """Attribute subattribute."""

    attribute_type_id: CURIE = Field(..., title="type")
    value: Any = Field(..., title="value")
    value_type_id: Optional[CURIE] = Field(
        None,
        title="value_type_id",
        nullable=True,
    )
    original_attribute_name: Optional[str] = Field(None, nullable=True)
    value_url: Optional[str] = Field(None, nullable=True)
    attribute_source: Optional[str] = Field(None, nullable=True)
    description: Optional[str] = Field(None, nullable=True)
    attributes: Optional[HashableSequence[RecursiveAttribute]] = Field(
        None, nullable=True
    )

    class Config:
        extra = "forbid"


class Attribute(BaseModel):
    """Node/edge attribute."""

    attribute_type_id: CURIE = Field(..., title="type")
    value: Any = Field(..., title="value")
    value_type_id: Optional[CURIE] = Field(
        None,
        title="value_type_id",
        nullable=True,
    )
    original_attribute_name: Optional[str] = Field(None, nullable=True)
    value_url: Optional[str] = Field(None, nullable=True)
    attribute_source: Optional[str] = Field(None, nullable=True)
    description: Optional[str] = Field(None, nullable=True)
    attributes: Optional[HashableSequence[SubAttribute]] = Field(None, nullable=True)

    class Config:
        extra = "forbid"


class BiolinkQualifier(ConstrainedStr):
    """Biolink Qualifier."""

    regex = re.compile("^biolink:[a-z][a-z_]*$")

    class Config:
        title = "biolink entity"


class Qualifier(BaseModel):
    """Edge qualifier."""

    qualifier_type_id: BiolinkQualifier = Field(..., title="type")

    qualifier_value: str = Field(..., title="value")


class BiolinkEntity(ConstrainedStr):
    """Biolink entity."""

    regex = re.compile("^biolink:[A-Z][a-zA-Z]*$")

    class Config:
        title = "biolink entity"


class BiolinkPredicate(ConstrainedStr):
    """Biolink predicate."""

    regex = re.compile("^biolink:[a-z][a-z_]*$")

    class Config:
        title = "biolink predicate"


class LogLevelEnum(str, Enum):
    """Log level."""

    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class LogLevel(BaseModel):
    """Log level."""

    __root__: LogLevelEnum


class LogEntry(BaseModel):
    """Log entry."""

    timestamp: Optional[datetime] = Field(None, nullable=True)
    level: Optional[LogLevel] = Field(None, nullable=True)
    code: Optional[str] = Field(None, nullable=True)
    message: Optional[str] = Field(None, nullable=True)

    class Config:
        extra = "allow"


RecursiveAttribute.update_forward_refs()
