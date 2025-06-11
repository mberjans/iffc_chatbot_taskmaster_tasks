"""
Knowledge Augmented Generation (KAG) Module.

This module implements the Knowledge Augmented Generation approach for the Nexus Scholar AI system,
which uses knowledge graphs to enhance the generation of answers to research questions.
"""

from .schema import (
    ENTITY_TYPES,
    RELATION_TYPES,
    validate_entity,
    validate_relation,
    get_entity_types,
    get_relation_types,
    get_entity_schema,
    get_relation_schema
)

from .library import (
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

from .ner import (
    NERTool,
    Entity,
    NERBackend,
    DummyNERBackend,
    BIOMEDICAL_ENTITY_TYPES,
    NER_BACKENDS
)

__all__ = [
    # Schema components
    'ENTITY_TYPES',
    'RELATION_TYPES',
    'validate_entity',
    'validate_relation',
    'get_entity_types',
    'get_relation_types',
    'get_entity_schema',
    'get_relation_schema',
    
    # Library components
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
    'get_library_info',
    
    # NER components
    'NERTool',
    'Entity',
    'NERBackend',
    'DummyNERBackend',
    'BIOMEDICAL_ENTITY_TYPES',
    'NER_BACKENDS'
]
