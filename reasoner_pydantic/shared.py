"""Shared models."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, constr, Field


class CURIE(BaseModel):
    """Compact URI."""

    __root__: str


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
    attributes: Optional[List[SubAttribute]] = Field(None, nullable=True)

    class Config:
        extra = "forbid"


class BiolinkEntity(BaseModel):
    """Biolink entity."""

    __root__: constr(regex='^biolink:[A-Z][a-zA-Z]*$')

    class Config:
        title = 'biolink entity'


class BiolinkPredicate(BaseModel):
    """Biolink predicate."""

    __root__: constr(regex="^biolink:[a-z][a-z_]*$")

    class Config:
        title = 'biolink predicate'


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
