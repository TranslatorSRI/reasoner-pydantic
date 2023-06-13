import collections.abc
from typing import Dict, List, Generic, Set, TypeVar

from pydantic.generics import GenericModel

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


class HashableMapping(
    GenericModel,
    Generic[KeyType, ValueType],
    collections.abc.MutableMapping,
):
    """
    Custom class that implements MutableMapping and is hashable
    """

    __root__: Dict[KeyType, ValueType] = dict()

    def __getitem__(self, k):
        return self.__root__[k]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def __setitem__(self, k, v):
        self.__root__[k] = v

    def __delitem__(self, k):
        del self.__root__[k]

    def __hash__(self):
        return hash(tuple((k, v) for k, v in self.__root__.items()))

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()


class HashableSequence(
    GenericModel,
    Generic[ValueType],
    collections.abc.MutableSequence,
):
    """
    Custom class that implements MutableSequence and is hashable
    """

    __root__: List[ValueType] = list()

    def __contains__(self, v):
        return v in self.__root__

    def __getitem__(self, i):
        return self.__root__[i]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def __setitem__(self, i, v):
        self.__root__[i] = v

    def __delitem__(self, i):
        del self.__root__[i]

    def insert(self, i, v):
        self.__root__.insert(i, v)

    def __hash__(self):
        return hash(tuple(self.__root__))

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()


class HashableSet(
    GenericModel,
    Generic[ValueType],
    collections.abc.MutableSet,
):
    """
    Custom class that implements MutableSet and is hashable
    """

    __root__: Set[ValueType] = set()

    def __contains__(self, v):
        return v in self.__root__

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def add(self, v):
        self.__root__.add(v)

    def update(self, other):
        self.__root__.update(other)

    def discard(self, v):
        self.__root__.discard(v)

    def __hash__(self):
        # Use frozenset instead of tuple to ensure
        # hash is computed without ordering of elements
        return hash(frozenset(self))

    def dict(self, *args, **kwargs):
        """Custom serialization method to convert to list"""

        # Normally, the dict method tries to cast to the __root__ type.
        # This isn't an issue for most __root__ types, but here that causes:
        # set({"hello" : "world"}) which doesn't work because dicts are not hashable
        # This overrides that functionality to cast to a list instead
        return [self._get_value(v, to_dict=True, **kwargs) for v in self]


def nonzero_validator(v):
    if v != None and len(v) == 0:
        raise ValueError("Must have nonzero number of elements")
    return v


def make_hashable(o):
    """
    Convert a generic Python object to a hashable one recursively

    This is an expensive operation, so it is best used sparingly
    """

    # type(o) is faster than isinstance(o) because it doesn't
    # traverse the inheritance hierarchy
    o_type = str(type(o))

    if "dict" in o_type:
        return HashableMapping.parse_obj(((k, make_hashable(v)) for k, v in o.items()))
    if "list" in o_type:
        return HashableSequence.parse_obj(make_hashable(v) for v in o)

    return o
