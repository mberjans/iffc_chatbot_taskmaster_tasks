"""
Knowledge Graph Library package for the KAG module.

This package contains the selected library and utilities for knowledge graph
construction and manipulation in the KAG module.
"""

from .kg_library import (
    KG_LIBRARY,
    create_knowledge_graph,
    add_entity,
    add_relation,
    get_entity,
    get_relations,
    get_entities_by_type,
    serialize_graph,
    deserialize_graph,
    save_graph,
    load_graph,
    get_library_info
)

__all__ = [
    'KG_LIBRARY',
    'create_knowledge_graph',
    'add_entity',
    'add_relation',
    'get_entity',
    'get_relations',
    'get_entities_by_type',
    'serialize_graph',
    'deserialize_graph',
    'save_graph',
    'load_graph',
    'get_library_info'
]
