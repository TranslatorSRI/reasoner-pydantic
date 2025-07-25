import collections.abc
from typing import Any, Collection, Generic, Iterable, Optional, TypeVar, cast

from pydantic import RootModel, model_serializer

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


class HashableMapping(
    RootModel[dict[KeyType, ValueType]],
    collections.abc.MutableMapping[KeyType, ValueType],
    Generic[KeyType, ValueType],
):
    """
    Custom class that implements MutableMapping and is hashable
    """

    root: dict[KeyType, ValueType] = dict()

    def __getitem__(self, k: KeyType) -> ValueType:
        return self.root[k]

    def __iter__(self):
        return iter(self.root)

    def __len__(self) -> int:
        return len(self.root)

    def __setitem__(self, k: KeyType, v: ValueType) -> None:
        self.root[k] = v

    def __delitem__(self, k: KeyType) -> None:
        del self.root[k]

    def __hash__(self):
        return hash(tuple((k, v) for k, v in self.root.items()))

    def __eq__(self, other: object) -> bool:
        return self.__hash__() == other.__hash__()


class HashableSequence(
    RootModel[list[ValueType]],
    collections.abc.MutableSequence[ValueType],
    Generic[ValueType],
):
    """
    Custom class that implements MutableSequence and is hashable
    """

    root: list[ValueType] = list()

    def __contains__(self, v: object) -> bool:
        return v in self.root

    def __getitem__(self, i):
        return self.root[i]

    def __iter__(self):
        return iter(self.root)

    def __len__(self):
        return len(self.root)

    def __setitem__(self, i, v) -> None:
        self.root[i] = v

    def __delitem__(self, i):
        del self.root[i]

    def insert(self, index, value):
        self.root.insert(index, value)

    def __hash__(self):
        return hash(tuple(self.root))

    def __eq__(self, other: object) -> bool:
        return self.__hash__() == other.__hash__()


class HashableSet(
    RootModel[set[ValueType]],
    collections.abc.MutableSet[ValueType],
    Generic[ValueType],
):
    """
    Custom class that implements MutableSet and is hashable
    """

    root: set[ValueType] = set()

    def __contains__(self, v):
        return v in self.root

    def __iter__(self):
        return iter(self.root)

    def __len__(self):
        return len(self.root)

    def add(self, value):
        self.root.add(value)

    def update(self, other: Iterable[ValueType]):
        self.root.update(other)

    def discard(self, value):
        self.root.discard(value)

    def __hash__(self):
        # Use frozenset instead of tuple to ensure
        # hash is computed without ordering of elements
        return hash(frozenset(self.root))

    @model_serializer
    def as_list(self) -> list[ValueType]:
        """Custom serialization method to convert to list"""

        # Normally, the dict method tries to cast to the root type.
        # This isn't an issue for most root types, but here that causes:
        # set({"hello" : "world"}) which doesn't work because dicts are not hashable
        # This overrides that functionality to cast to a list instead
        return list(self.root)


def nonzero_validator(v: Optional[Collection[Any]]):
    if v is not None and len(v) == 0:
        raise ValueError("Must have nonzero number of elements")
    return v


def make_hashable(o: object):
    """
    Convert a generic Python object to a hashable one recursively

    This is an expensive operation, so it is best used sparingly
    """

    # type(o) is faster than isinstance(o) because it doesn't
    # traverse the inheritance hierarchy
    o_type = str(type(o))

    if "dict" in o_type:
        return HashableMapping(
            {k: make_hashable(v) for k, v in cast(dict[Any, Any], o).items()}
        )
    if "list" in o_type:
        return HashableSequence([make_hashable(v) for v in cast(list[Any], o)])

    return o
