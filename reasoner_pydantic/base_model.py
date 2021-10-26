import collections

from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    """ Custom base model for all classes """
