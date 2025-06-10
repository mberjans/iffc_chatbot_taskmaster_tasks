"""
Knowledge Graph Schema package for the KAG module.

This package contains definitions and utilities for the Knowledge Graph schema
used in the Knowledge Augmented Generation (KAG) module.
"""

from .kg_schema import (
    ENTITY_TYPES,
    RELATION_TYPES,
    validate_entity,
    validate_relation,
    get_entity_types,
    get_relation_types,
    get_entity_schema,
    get_relation_schema
)

__all__ = [
    'ENTITY_TYPES',
    'RELATION_TYPES',
    'validate_entity',
    'validate_relation',
    'get_entity_types',
    'get_relation_types',
    'get_entity_schema',
    'get_relation_schema'
]
