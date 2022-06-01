from collections import defaultdict


def upgrade_from_1p2(old_dict, result_source="ARA", result_method="default"):
    def edge_conversion(kedge):
        kedge = dict(kedge)
        ksubject = kedge.get("subject")
        kpredicate = kedge.get("predicate")
        kobject = kedge.get("object")
        kqualifiers = []
        hashing_qualifiers = []
        ksource = None
        provenance_tree = []
        knegated = kedge.get("negated", False)
        kattributes = []

        # Separate source attributes from regular attributes
        source_attribute_types = [
            "biolink:knowledge_source",  # This is not intended to be used but is
            "biolink:primary_knowledge_source",
            "biolink:original_knowledge_source",
            "biolink:aggregator_knowledge_source",
        ]
        source_attributes = []
        attrs = list(kedge.get("attributes"))
        removals = []
        for attribute in attrs:
            attr_type = attribute.get("attribute_type_id", None)
            if attr_type in source_attribute_types:
                removals.append(attribute)  # Remove them from the original list
                source_attributes.append(attribute)
        for r in removals:
            attrs.remove(r)
        # attrs are now all the attributes we want to use
        # We need to build the resouce and retrievals chain from the sources

        # Find the root source (original or primary)
        root_source = None
        for i, source in enumerate(source_attributes):
            attr_type = source.get("attribute_type_id")
            if attr_type == "biolink:original_knowledge_source":
                root_source = source
                source_attributes.pop(i)
                break
            if attr_type == "biolink:primary_knowledge_source":
                root_source = source
                source_attributes.pop(i)
                break
        if not root_source and source_attributes:
            # As a fail safe just use the first one as the root?
            root_source = source_attributes.pop(0)

        if not root_source:
            # Still no sources
            new_sources = []
        else:
            # Build the list of sources with retrievals
            # Assume order has meaning?
            v = root_source["value"]
            if isinstance(v, list):
                v = v[0]
            new_sources = [
                {
                    "resource": v,
                    "resource_role": root_source["attribute_type_id"],
                    "retrievals": [],
                }
            ]
            for source in source_attributes:
                v = source["value"]
                if isinstance(v, list):
                    v = v[0]
                new_sources[-1]["retrievals"].append({"retrieved_from": v})

                new_sources.append(
                    {
                        "resource": v,
                        "resource_role": source["attribute_type_id"],
                        "retrievals": [],
                    }
                )

        edge_key = hash(
            (
                ksubject,
                kobject,
                kpredicate,
                knegated,
                tuple(hashing_qualifiers),
                ksource,
            )
        )
        converted_edge = {
            "subject": ksubject,
            "predicate": kpredicate,
            "object": kobject,
            "negated": knegated,
            "qualifiers": kqualifiers,
            "sources": new_sources,
            "attributes": attrs,
        }
        return edge_key, converted_edge

    # Actually do the upgrading
    kg = old_dict["knowledge_graph"]
    new_edges = dict()
    edge_key_map = dict()
    for old_key, old_edge in kg["edges"].items():
        edge_key, converted_edge = edge_conversion(old_edge)
        edge_key_map[old_key] = edge_key
        new_edges[edge_key] = converted_edge

    new_results = []
    for r in old_dict["results"]:
        node_binding_attributes = defaultdict(dict)
        edge_binding_attributes = defaultdict(dict)

        for k, eb in r["edge_bindings"].items():

            # Update edge bindings to new KG edge keys
            for b in eb:
                b_a = b.pop("attributes", None)
                if b_a:
                    edge_binding_attributes[k][edge_key_map[b["id"]]] = b_a

                b["id"] = edge_key_map[b["id"]]  # edit binding in place to new edge key

        for k, nb in r["node_bindings"].items():
            for b in nb:
                b_a = b.pop("attributes", None)
                if b_a:
                    node_binding_attributes[k][b["id"]] = b_a

        score = r.pop("score", None)

        new_r = {
            "node_bindings": r["node_bindings"],
            "edge_bindings": r["edge_bindings"],
            "analyses": [
                {
                    "resource": result_source,
                    "method": result_method,
                    "node_binding_attributes": node_binding_attributes,
                    "edge_binding_attributes": edge_binding_attributes,
                    "score": score,
                }
            ],
        }
        new_results.append(new_r)

    new_kg = kg
    new_kg["edges"] = new_edges

    new_dict = {
        "query_graph": old_dict["query_graph"],
        "knowledge_graph": new_kg,
        "results": new_results,
    }
    return new_dict
