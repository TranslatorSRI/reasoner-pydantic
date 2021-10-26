from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    """ Custom base model for all classes """

    def __hash__(self) -> int:
        """ Hash function based on Pydantic implementation """
        # if hasattr(self, "__root__"):
        #     return hash(self.__root__)
        return hash(self.__class__) + hash(tuple(self.__dict__.values()))
