import collections
from typing import Callable, Dict, List, Generic, TypeVar

from pydantic import PrivateAttr
from pydantic.generics import GenericModel

KeyType = TypeVar('KeyType')
ValueType = TypeVar('ValueType')

class HashableMapping(GenericModel, Generic[KeyType, ValueType]):
    """
    Custom class that implements MutableMapping and is hashable

    Hash will be recomputed if items are updated or deleted. The
    hash can be considered valid if the values are immutable.
    """
    __root__: Dict[KeyType, ValueType]

    _hash: int = PrivateAttr(default=None)
    _invalidate_hook: Callable = PrivateAttr(default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value in self.__root__.values():
            if hasattr(value, "_invalidate_hook"):
                value._invalidate_hook = self.invalidate_hash

    def __getitem__(self, k):
        return self.__root__[k]
    def __iter__(self):
        return iter(self.__root__)
    def __len__(self):
        return len(self.__root__)

    def __setitem__(self, k, v):
        self.invalidate_hash()
        if hasattr(v, "_invalidate_hook"):
            v._invalidate_hook = self.invalidate_hash
        self.__root__[k] = v
    def __delitem__(self, k):
        self.invalidate_hash()
        del self.__root__[k]

    def __hash__(self):
        if self._hash is None:
            h = 0
            for key, value in self.__root__.items():
                h ^= hash((key, value))
            self._hash = h
        return self._hash

    def invalidate_hash(self):
        """ Invalidate stored hash value """
        self._hash = None
        # Propogate
        if self._invalidate_hook:
            self._invalidate_hook()


class HashableSequence(GenericModel, Generic[ValueType]):
    """
    Custom class that implements MutableSequence and is hashable

    Hash will be recomputed if items are updated or deleted. The
    hash can be considered valid if the values are immutable.
    """
    __root__: List[ValueType]
    _hash: int = PrivateAttr(default=None)
    _invalidate_hook: Callable = PrivateAttr(default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value in self.__root__:
            if hasattr(value, "_invalidate_hook"):
                value._invalidate_hook = self.invalidate_hash

    def __getitem__(self, i):
        return self.__root__[i]
    def __iter__(self):
        return iter(self.__root__)
    def __len__(self):
        return len(self.__root__)

    def __setitem__(self, i, v):
        self.invalidate_hash()
        if hasattr(v, "_invalidate_hook"):
            v._invalidate_hook = self.invalidate_hash
        self.__root__[i] = v
    def __delitem__(self, i):
        self.invalidate_hash()
        del self.__root__[i]
    def insert(self, i, v):
        self.invalidate_hash()
        self.__root__.insert(i, v)

    def __hash__(self):
        if self._hash is None:
            h = 0
            for value in self.__root__:
                h ^= hash(value)
            self._hash = h
        return self._hash

    def invalidate_hash(self):
        """ Invalidate stored hash value """
        self._hash = None
        # Propogate
        if self._invalidate_hook:
            self._invalidate_hook()

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

