# Reasoner-Pydantic

[![Test status via GitHub Actions](https://github.com/TranslatorSRI/reasoner-pydantic/workflows/test/badge.svg)](https://github.com/TranslatorSRI/reasoner-pydantic/actions?query=workflow%3Atest) [ℹ️](tests/README.md)

[Pydantic](https://pydantic-docs.helpmanual.io/) models for the [Reasoner API](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI) data formats.

These models are very handy when setting up a Reasoner API with [FastAPI](https://fastapi.tiangolo.com/).

These models provide validation for TRAPI messages, as well as useful utilities based on architectural decisions, such as edge merging, result merging, and analysis combination.

## Example usage

```python
from reasoner_pydantic import (
    Query,
    Message,
    Node,
    Result,
    CURIE,
)


def add_result_to_query(query_dict):
    query = Query.model_validate(query_dict)
    message: Message = query.message

    # get query graph node
    qnode_id = next(iter(message.query_graph.nodes))

    # add knowledge graph node
    knode = Node.model_validate({"categories": ["biolink:FooBar"]})
    knode_id = CURIE("foo:bar")
    message.knowledge_graph.nodes[knode_id] = knode

    # add result
    result: Result = Result.model_validate({"node_bindings": {qnode_id: [{"id": knode_id}]}})

    message.results.add(result)

    return message.model_dump_json()


add_result_to_query(
    {
        "message": {
            "query_graph": {"nodes": {"n0": {}}, "edges": {}},
            "knowledge_graph": {"nodes": {}, "edges": {}},
            "results": [],
        }
    }
)
```

## Validation Usage

Typically, you'll want to instantiate models using `<ModelName>.model_validate(<data>)`:

```python
from reasoner_pydantic import KnowledgeGraph

# In Python dict format
kg = KnowledgeGraph.model_validate(<your kg dict here>)
# In raw JSON
kg = KnowledgeGraph.model_validate_json(<your kg JSON string here>)
```

You can also directly instantiate models, however it's not quite as clean:

```python
from reasoner_pydantic import KnowledgeGraph

kg = KnowledgeGraph(nodes=<your nodes here>, edges=<your edges here>)
```

In all of these cases, validation is automatically done. In most use-cases it's recommended to use `model_validate()` as the performance cost is much lower than in pydantic v1. However, if you're absolutely certain your data is valid, you can construct a model without validation:

```python
from reasoner_pydantci import KnowledgeGraph

kg = KnowledgeGraph.model_construct(nodes="fake")
# Won't throw errors
```

> [!WARNING]
> All values passed to `model_construct()` will not be transformed into their appropriate models.
> Pydantic's documentation states that it's often *more* performant to use `model_validate()`,
> so it's highly recommended to avoid using this method.

This is especially important to keep in mind when constructing objects that use containers.
This library uses custom container types: HashableMapping, HashableSequence, HashableSet:

```python
from reasoner_pydantic import KnowledgeGraph, Node, CURIE

# This is not correct and will not throw an error, but will cause problems later
kg = KnowledgeGraph(nodes = {})

# Instead, if you would like to build models this way, use a typed container constructor
kg = KnowledgeGraph(nodes = HashableMapping[CURIE, Node]())
```

For this reason, we recommend one of the following options:

1. Use `model_validate()` exclusively for constructing models. This will perform validation for you. This option is best if performance is not important.
1. Use a static type checker to ensure that models are being constructed correctly. Constructing objects this way is more performant, and the static type checker will ensure that it is done correctly. We recommend using [pyright](https://github.com/microsoft/pyright) in your editor.
