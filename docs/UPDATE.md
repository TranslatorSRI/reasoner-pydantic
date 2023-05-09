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

To achieve this, we have a [custom base model](reasoner_pydantic/base_model.py) for all objects that includes a hash function. This hash function recurses down through the object and computes the hash for the entire object when called. We have similar code in place for lists, dicts, and sets, which can be found in the [reasoner_pydantic/utils.py](reasoner_pydantic/utils.py) file. When implemented properly, this provide the basis for efficient in-place object merging.

To ensure deterministic hash values, it is required that the `PYTHONHASHSEED` environemntal variable be set to `0`.


