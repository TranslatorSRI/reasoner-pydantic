"""Shared models."""
import re
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import Field
from pydantic.types import ConstrainedStr

from .base_model import BaseModel
from .utils import HashableSequence


class CURIE(str):
    """Compact URI."""


class EdgeIdentifier(str):
    """Identifier for an edge in a knowledge graph"""


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
