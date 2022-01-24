# Reasoner-Pydantic

[![Test status via GitHub Actions](https://github.com/TranslatorSRI/reasoner-pydantic/workflows/test/badge.svg)](https://github.com/TranslatorSRI/reasoner-pydantic/actions?query=workflow%3Atest) [ℹ️](tests/README.md)

[Pydantic](https://pydantic-docs.helpmanual.io/) models for the [Reasoner API](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI) data formats.

These models are very handy when setting up a Reasoner API with [FastAPI](https://fastapi.tiangolo.com/).

## Example usage

```python
from reasoner_pydantic import (
    Query,
    Message,
    QNode,
    KnowledgeGraph,
    Node,
    Result,
    NodeBinding,
)


def add_result_to_query(query_dict):
    query = Query.parse_obj(query_dict)
    message: Message = query.message

    # get query graph node
    qnode_id = next(iter(message.query_graph.nodes))

    # add knowledge graph node
    knode = Node.parse_obj({"categories": ["biolink:FooBar"]})
    knode_id = "foo:bar"
    message.knowledge_graph.nodes[knode_id] = knode

    # add result
    result: Result = Result.parse_obj(
        {
            "node_bindings": {qnode_id: [{"id": knode_id}]},
            "edge_bindings": {},
        }
    )

    message.results.add(result)

    return message.json()


add_result_to_query({
    "message": {
        "query_graph": {"nodes": {"n0": {}}, "edges": {}},
        "knowledge_graph": {"nodes": {}, "edges": {}},
        "results" : []
    }
})
```

## Validation Usage

Because of performance concerns, as well as how types are implemented in Python, there is no assignment validation enforced on these models.
For example:

```python
from reasoner_pydantic import KnowledgeGraph

# This will not throw an error
kg = KnowledgeGraph(nodes = "hi")
```

This is especially important to keep in mind when constructing objects that use containers.
This library uses custom container types: HashableMapping, HashableSequence, HashableSet:

```python
from reasoner_pydantic import KnowledgeGraph, Node, CURIE

# This is not correct and will not throw an error, but will cause problems later
kg = KnowledgeGraph(nodes = {})

# Instead, if you would like to build models this way, use a typed container constructor
kg = KnowledgeGraph(nodes = HashableMapping[CURIE, Node](__root__ = {}))
```

For this reason, we recommend one of the following options:

1. Use `parse_obj` exclusively for constructing models. This will perform validation for you. This option is best if performance is not important.
2. Use a static type checker to ensure that models are being constructed correctly. Constructing objects this way is more performant, and the static type checker will ensure that it is done correctly. We recommend using [pyright](https://github.com/microsoft/pyright) in your editor.
