# pylint: disable=too-few-public-methods, missing-class-docstring
"""Shared models."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, constr, Field


class CURIE(BaseModel):
    """Compact URI."""

    __root__: str


class Attribute(BaseModel):
    """Node/edge attribute."""

    type: CURIE = Field(..., title="type")
    value: Any = Field(..., title="value")
    name: Optional[str] = Field(None, nullable=True)
    url: Optional[str] = Field(None, nullable=True)
    source: Optional[str] = Field(None, nullable=True)

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


class LevelEnum(str, Enum):
    """Logging level."""

    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class LogEntry(BaseModel):
    """Log entry."""

    timestamp: Optional[datetime] = Field(None, nullable=True)
    level: Optional[str] = Field(None, nullable=True)
    code: Optional[str] = Field(None, nullable=True)
    message: Optional[str] = Field(None, nullable=True)

    class Config:
        @staticmethod
        def schema_extra(schema: Dict[str, Any], _) -> None:
            """Modify generated schema."""
            schema["properties"]["level"].update({
                "type": "string",
                "enum": [
                    "ERROR",
                    "WARNING",
                    "INFO",
                    "DEBUG",
                ]
            })
