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
