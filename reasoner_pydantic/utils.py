import collections
from typing import Callable, Dict, List, Generic, Set, TypeVar

from pydantic import PrivateAttr
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
            self._hash = hash(tuple((k, v) for k, v in self.__root__.items()))
        return self._hash

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()

    def invalidate_hash(self):
        """Invalidate stored hash value"""
        self._hash = None
        # Propogate
        if self._invalidate_hook:
            self._invalidate_hook()


class HashableSequence(
    GenericModel,
    Generic[ValueType],
    collections.abc.MutableSequence,
):
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
            self._hash = hash(tuple(self.__root__))
        return self._hash

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()

    def invalidate_hash(self):
        """Invalidate stored hash value"""
        self._hash = None
        # Propogate
        if self._invalidate_hook:
            self._invalidate_hook()


class HashableSet(
    GenericModel,
    Generic[ValueType],
    collections.abc.MutableSet,
):
    """
    Custom class that implements MutableSet and is hashable

    Hash will be recomputed if items are updated or deleted. The
    hash can be considered valid if the values are immutable.
    """

    __root__: Set[ValueType]
    _hash: int = PrivateAttr(default=None)
    _invalidate_hook: Callable = PrivateAttr(default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for value in self.__root__:
            if hasattr(value, "_invalidate_hook"):
                value._invalidate_hook = self.invalidate_hash

    def __contains__(self, v):
        return v in self.__root__

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def add(self, v):
        self.invalidate_hash()
        if hasattr(v, "_invalidate_hook"):
            v._invalidate_hook = self.invalidate_hash
        self.__root__.add(v)

    def update(self, other):
        self.invalidate_hash()
        self.__root__.update(other)

    def discard(self, v):
        self.invalidate_hash()
        self.__root__.discard(v)

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(self.__root__))
        return self._hash

    def invalidate_hash(self):
        """Invalidate stored hash value"""
        self._hash = None
        # Propogate
        if self._invalidate_hook:
            self._invalidate_hook()

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
