import collections

from pydantic import BaseModel as PydanticBaseModel


class FrozenDict(dict):
    """
    Dict class that can be used as a key (hashable)

    This class provides NO enforcement for mutation
    """
    def __init__(self, *args, **kwargs):
        self._key = None
        super().__init__(*args, **kwargs)

    def __key(self):
        # Use cache for key
        if not self._key:
            self._key = tuple((k, self[k]) for k in sorted(self))
        return self._key

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()


def freeze_object(o, setify):
    """
    Freeze an object recursively

    Either converts lists to sets (unordered) or to tuples (ordered)
    """
    if isinstance(o, BaseModel):
        new_object = o.frozendict(setify)
    elif isinstance(o, collections.abc.Mapping):
        new_object = FrozenDict({
            k: freeze_object(v, setify)
            for k, v in o.items()
        })
    elif (
            isinstance(o, collections.abc.Sequence)
            and
            not isinstance(o, str)
            ):
        if setify:
            new_object = frozenset(
                freeze_object(v, setify) for v in o
            )
        else:
            new_object = tuple(
                freeze_object(v, setify) for v in o
            )
    else:
        new_object = o

    return new_object

class BaseModel(PydanticBaseModel):
    """ Custom base model for all classes """

    def frozendict(self, setify=False):
        """
        Same as .dict() method, but outputs hashable dictionaries

        Choice to convert list fields to tuples or sets with setify
        """
        if hasattr(self, "__root__"):
            return freeze_object(self.__root__, setify)
        return FrozenDict({
            key: freeze_object(value, setify)
            for key, value in self
        })
