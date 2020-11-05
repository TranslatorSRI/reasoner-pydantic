# pylint: disable=too-few-public-methods, missing-class-docstring
"""Shared models."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Type

from pydantic import BaseModel, constr, Field


class Attribute(BaseModel):
    """Node/edge attribute."""

    type: str = Field(..., title="type")
    value: Any = Field(..., title="value")
    name: str = None
    url: str = None
    source: str = None

    class Config:
        extra = "forbid"


class BiolinkEntity(BaseModel):
    """Biolink entity."""

    __root__: constr(regex='^biolink:[A-Z][a-zA-Z]*$')

    class Config:
        title = 'biolink entity'


class BiolinkRelation(BaseModel):
    """Biolink relation."""

    __root__: constr(regex="^biolink:[a-z][a-z_]*$")

    class Config:
        title = 'biolink relation'


class CURIE(BaseModel):
    """Compact URI."""

    __root__: str


class LevelEnum(str, Enum):
    """Logging level."""

    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class LogEntry(BaseModel):
    """Log entry."""

    timestamp: datetime = None
    level: LevelEnum = None
    code: str = None
    message: str = None

    class Config:
        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: Type['Person']) -> None:
            """Modify generated schema."""
            schema["properties"]["level"] = {
                "type": "string",
                "enum": [
                    "ERROR",
                    "WARNING",
                    "INFO",
                    "DEBUG",
                ]
            }
