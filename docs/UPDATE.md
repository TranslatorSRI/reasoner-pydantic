# Update Method

The .update() method enables fast, in-place message merging. This means merging messages from potentially thousands of KPs. During this merging, it is important that certain parts of the message, such as results and node categories, are deduplicated.

The only way to handle deduplication efficiently is to make objects hashable. This enables fast comparisons that would otherwise be too costly. However, Pydantic's built in hash functions are only enabled for immutable objects. This creates another problem because immutable objects cannot be merged in place, they need to be copied. This copying is also too costly for merging thousands of objects together.

Our solution to this was to develop custom Pydantic models that implement a hash function and are still mutable. Here is an example from a test:

```python
def test_hash_property_update():
    """Check that we can update the property of an object and the hash changes"""

    # Test on a QNode
    qnode = QNode.parse_obj({"categories": ["biolink:ChemicalSubstance"]})

    h = hash(qnode)

    qnode.is_set = True

    assert hash(qnode) != h
```

There are two ways to achieve this result. One is to define a hash function which recomputes the hash every time it is called. Another is to save the computed hash to the object and then remove the saved hash if there is a change. Currently, reasoner-pydantic uses the second method. To implement this, it is important to invalidate the hash if the object, or any children of the object, change. Here is another example:

```python
def test_hash_deeply_nested_update():
    """
    Check that we can update a deeply nested object and the hash change is propogated
    """

    m = Message.parse_obj(EXAMPLE_MESSAGE)
    h = hash(m)

    m.query_graph.nodes["n1"].categories.append(BiolinkEntity.parse_obj("biolink:Gene"))

    assert hash(m) != h
```

We have to ensure that a deeply nested change is propogated upwards to invalidate the hash of all parent objects. To achieve this, we have a [custom base model](reasoner_pydantic/base_model.py) for all objects that looks something like this:

```python
class BaseModel(PydanticBaseModel):
    _hash: int
    _invalidate_hook: Callable
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Give nested objects a hook that they
        # can use to invalidate hash on this object
        for value in self.__dict__.values():
            if hasattr(value, "_invalidate_hook"):
                value._invalidate_hook = self.invalidate_hash

    def invalidate_hash(self):
        """Invalidate stored hash value"""
        self._hash = None
        # Propogate
        if self._invalidate_hook:
            self._invalidate_hook()

    def __setattr__(self, name, value):
        """Custom setattr that invalidates hash"""
        self.invalidate_hash()
        return super().__setattr__(name, value)
```

We have similar code in place for lists, dicts, and sets, which can be found in the [reasoner_pydantic/utils.py](reasoner_pydantic/utils.py) file. When implemented properly, these methods provide the basis for efficient in-place object merging.
