# pylint: disable=too-few-public-methods, missing-class-docstring
"""Basic type models."""
from pydantic import BaseModel, constr


class BiolinkEntity(BaseModel):
    """Biolink entity."""

    __root__: constr(regex='^.+:.+$')

    class Config:
        title = 'biolink entity'


class BiolinkRelation(BaseModel):
    """Biolink relation."""

    __root__: str

    class Config:
        title = 'biolink relation'
