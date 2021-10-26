import collections
from typing import Dict, List, Generic, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic.fields import ModelField

KeyType = TypeVar('KeyType')
ValueType = TypeVar('ValueType')

class HashableMapping(PydanticBaseModel, Generic[KeyType, ValueType]):
    """
    Custom class that implements MutableMapping and is hashable

    Hash will be recomputed if items are updated or deleted. The
    hash can be considered valid if the values are immutable.
    """
    __root__: Dict[KeyType, ValueType]

    _hash = None

    def __getitem__(self, k):
        return self.__root__[k]
    def __iter__(self):
        return iter(self.__root__)
    def __len__(self):
        return len(self.__root__)

    def __setitem__(self, k, v):
        # Invalidate hash
        self._hash = None
        self.__root__[k] = v
    def __delitem__(self, k):
        # Invalidate hash
        self._hash = None
        del self.__root__[k]

    def __hash__(self):
        if self._hash is None:
            h = 0
            for key, value in self.__root__.items():
                h ^= hash((key, value))
            self._hash = h
        return self._hash

    def __repr__(self):
        return repr(self.__root__)


class HashableSequence(PydanticBaseModel, Generic[ValueType]):
    """
    Custom class that implements MutableSequence and is hashable

    Hash will be recomputed if items are updated or deleted. The
    hash can be considered valid if the values are immutable.
    """
    __root__: List[ValueType]

    _hash = None

    def __getitem__(self, i):
        return self.__root__[i]
    def __iter__(self):
        return iter(self.__root__)
    def __len__(self):
        return len(self.__root__)

    def __setitem__(self, i, v):
        # Invalidate hash
        self._hash = None
        self.__root__[i] = v
    def __delitem__(self, i):
        # Invalidate hash
        self._hash = None
        del self.__root__[i]
    def insert(self, i, v):
        # Invalidate hash
        self._hash = None
        self.__root__.insert(i, v)

    def __hash__(self):
        if self._hash is None:
            h = 0
            for value in self.__root__:
                h ^= hash(value)
            self._hash = h
        return self._hash

def make_hashable(o):
    """
    Convert a generic Python object to a hashable one recursively

    This is an expensive operation, so it is best used sparingly
    """

    # type(o) is faster than isinstance(o) because it doesn't
    # traverse the inheritance hierarchy
    o_type = str(type(o))

    if "dict" in o_type:
        return HashableMapping((
            (k, make_hashable(v))
            for k,v in o.items()
        ))
    if "list" in o_type:
        return HashableSequence(
            make_hashable(v)
            for v in o
        )

    return o

