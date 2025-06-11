"""
Named Entity Recognition (NER) package for the KAG Module.

This package provides tools and utilities for biomedical named entity recognition
to support the Knowledge Augmented Generation (KAG) module.
"""

from .entities import (
    BIOMEDICAL_ENTITY_TYPES,
    NER_BACKENDS
)

from .ner_tool import (
    Entity,
    NERBackend,
    DummyNERBackend,
    NERTool
)

__all__ = [
    # Entity Types
    'BIOMEDICAL_ENTITY_TYPES',
    'NER_BACKENDS',
    
    # Core Classes
    'Entity',
    'NERBackend',
    'DummyNERBackend',
    'NERTool'
]
