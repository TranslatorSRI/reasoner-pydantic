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
        for attribute in kedge.get("attributes"):
            if "biolink:original_knowledge_source" == attribute.get(
                "attribute_type_id"
            ):
                ksource = attribute["value"]
                attribute["attribute_type_id"] = "biolink:primary_knowledge_source"
                if provenance_tree:
                    last = provenance_tree[len(provenance_tree) - 1]
                    for i in range(len(provenance_tree) - 1, 1, -1):
                        if provenance_tree[i]["resource"] == attribute.get(
                            "attribute_source"
                        ):
                            provenance_tree[1], provenance_tree[i] = (
                                provenance_tree[i],
                                provenance_tree[1],
                            )
                        provenance_tree[i] = provenance_tree[i - 1]
                    provenance_tree[0] = {
                        "resource": attribute["value"],
                        "resource_role": attribute["attribute_type_id"],
                    }
                    provenance_tree[1]["retrievals"] = provenance_tree[0]["resource"]
                    provenance_tree.append(last)
                else:
                    provenance_tree.append(
                        {
                            "resource": attribute["value"],
                            "resource_role": attribute["attribute_type_id"],
                        }
                    )
            elif "biolink:primary_knowledge_source" == attribute["attribute_type_id"]:
                ksource = attribute["value"]
                if provenance_tree:
                    last = provenance_tree[len(provenance_tree) - 1]
                    for i in range(len(provenance_tree) - 1, 1, -1):
                        if provenance_tree[i]["resource"] == attribute.get(
                            "attribute_source"
                        ):
                            provenance_tree[1], provenance_tree[i] = (
                                provenance_tree[i],
                                provenance_tree[1],
                            )
                        provenance_tree[i] = provenance_tree[i - 1]
                    provenance_tree[0] = {
                        "resource": attribute["value"],
                        "resource_role": attribute["attribute_type_id"],
                    }
                    provenance_tree[1]["retrievals"] = provenance_tree[0]["resource"]
                    provenance_tree.append(last)
                else:
                    provenance_tree.append(
                        {
                            "resource": attribute["value"],
                            "resource_role": attribute["attribute_type_id"],
                        }
                    )
            elif attribute["attribute_type_id"] == "biolink:qualifiers":
                hashing_qualifiers.append(attribute["value"])
                kqualifiers.append(attribute)
            elif (
                attribute["attribute_type_id"] == "biolink:aggregator_knowledge_source"
            ):
                if provenance_tree:
                    check = True
                    for source in provenance_tree:
                        if source["resource"] == attribute.get("attribute_source"):
                            provenance_tree.append(
                                provenance_tree[len(provenance_tree) - 1]
                            )
                            source["retrievals"] = attribute["value"]
                            source_index = provenance_tree.index(source)
                            for i in range(
                                len(provenance_tree) - 1, source_index + 1, -1
                            ):
                                provenance_tree[i] = provenance_tree[i - 1]
                            provenance_tree[source_index] = {
                                "resource": attribute["value"],
                                "resource_role": attribute["attribute_type_id"],
                            }
                            check = False
                            break
                    if check:
                        provenance_tree.append(
                            {
                                "resource": attribute["value"],
                                "resource_role": attribute["attribute_type_id"],
                                "retrievals": [
                                    provenance_tree[len(provenance_tree) - 1][
                                        "resource"
                                    ]
                                ],
                            }
                        )
                else:
                    provenance_tree.append(
                        {
                            "resource": attribute["value"],
                            "resource_role": attribute["attribute_type_id"],
                        }
                    )
            else:
                kattributes.append(attribute)
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
            "object": kpredicate,
            "negated": knegated,
            "qualifiers": kqualifiers,
            "sources": provenance_tree,
            "attributes": kattributes,
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
                    "source": result_source,
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
