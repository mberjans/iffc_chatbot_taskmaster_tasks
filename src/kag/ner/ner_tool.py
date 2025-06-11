"""
Named Entity Recognition (NER) Tool for the KAG Module.

This module provides functionality for biomedical named entity recognition
to extract entities such as genes, proteins, diseases, chemicals, and other
biomedical concepts from text.
"""

import logging
import re
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional, Set, Union

from .entities import BIOMEDICAL_ENTITY_TYPES, NER_BACKENDS

# Configure logging
logger = logging.getLogger(__name__)

class Entity:
    """
    Class representing a named entity extracted from text.
    """
    
    def __init__(
        self,
        text: str,
        entity_type: str,
        start_char: int,
        end_char: int,
        source_text: str = None
    ):
        """
        Initialize an entity.
        
        Args:
            text (str): The entity text
            entity_type (str): The type of entity (e.g., "GENE", "DISEASE")
            start_char (int): The start position of the entity in the source text
            end_char (int): The end position of the entity in the source text
            source_text (str, optional): The source text from which the entity was extracted
        """
        self.text = text
        self.entity_type = entity_type
        self.start_char = start_char
        self.end_char = end_char
        self.source_text = source_text
    
    def get_context(self, window: int = 50) -> str:
        """
        Get the context surrounding this entity in the source text.
        
        Args:
            window (int): Number of characters to include before and after the entity
            
        Returns:
            str: The context string or empty string if no source text is available
        """
        if not self.source_text:
            return ""
        
        start = max(0, self.start_char - window)
        end = min(len(self.source_text), self.end_char + window)
        
        return self.source_text[start:end]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the entity to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representing this entity
        """
        return {
            "text": self.text,
            "entity_type": self.entity_type,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "description": BIOMEDICAL_ENTITY_TYPES.get(self.entity_type, self.entity_type)
        }
    
    def __str__(self) -> str:
        return f"{self.text} ({self.entity_type}) [{self.start_char}:{self.end_char}]"
    
    def __repr__(self) -> str:
        return self.__str__()


class NERBackend(ABC):
    """
    Abstract base class for NER backends.
    
    This class defines the interface that all NER backends must implement.
    """
    
    @abstractmethod
    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract entities from the given text.
        
        Args:
            text (str): Text to extract entities from
            
        Returns:
            List[Entity]: List of extracted entities
        """
        pass
    
    @property
    @abstractmethod
    def supported_entity_types(self) -> List[str]:
        """
        Get the list of entity types supported by this backend.
        
        Returns:
            List[str]: List of supported entity types
        """
        pass
    
    @property
    @abstractmethod
    def backend_name(self) -> str:
        """
        Get the name of this backend.
        
        Returns:
            str: Name of the backend
        """
        pass


class DummyNERBackend(NERBackend):
    """
    A simple pattern-based NER backend for demonstration purposes.
    
    This backend uses simple regular expressions to detect entities.
    It is not intended for production use, but rather as a fallback
    when more sophisticated backends are not available.
    """
    
    def __init__(self):
        """Initialize the dummy NER backend with simple patterns."""
        self._patterns = {
            "GENE": r'\b[A-Z0-9]{2,}[0-9]?\b',  # Simple pattern for gene symbols like "BRCA1"
            "DISEASE": r'\b(cancer|disease|syndrome|disorder)\b',  # Simple disease terms
            "CHEMICAL": r'\b[A-Z][a-z]*(?:acid|ine|ol|ate|ide)\b'  # Simple chemical name patterns
        }
        
        self._compiled_patterns = {
            entity_type: re.compile(pattern, re.IGNORECASE)
            for entity_type, pattern in self._patterns.items()
        }
    
    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract entities using simple pattern matching.
        
        Args:
            text (str): Text to extract entities from
            
        Returns:
            List[Entity]: List of extracted entities
        """
        if not text or not text.strip():
            return []
        
        entities = []
        
        for entity_type, pattern in self._compiled_patterns.items():
            for match in pattern.finditer(text):
                start, end = match.span()
                entity_text = match.group()
                
                entities.append(Entity(
                    text=entity_text,
                    entity_type=entity_type,
                    start_char=start,
                    end_char=end,
                    source_text=text
                ))
        
        return sorted(entities, key=lambda e: e.start_char)
    
    @property
    def supported_entity_types(self) -> List[str]:
        """Get the list of entity types supported by this backend."""
        return list(self._patterns.keys())
    
    @property
    def backend_name(self) -> str:
        """Get the name of this backend."""
        return "dummy"


class NERTool:
    """
    Named Entity Recognition Tool for biomedical text.
    
    This class provides methods for extracting entities from text and
    processing documents for entity recognition using various backends.
    """
    
    def __init__(self, backend: str = "dummy"):
        """
        Initialize the NER Tool with the specified backend.
        
        Args:
            backend (str): Name of the backend to use (default: dummy)
        
        Raises:
            ValueError: If the specified backend is not supported
            ImportError: If the required backend cannot be loaded
        """
        self.backend_name = backend
        
        if backend not in NER_BACKENDS:
            supported_backends = ", ".join(NER_BACKENDS.keys())
            raise ValueError(f"Backend '{backend}' not supported. Available backends: {supported_backends}")
        
        self.backend_info = NER_BACKENDS[backend]
        
        # Initialize the appropriate backend
        if backend == "dummy":
            self.backend = DummyNERBackend()
        elif backend == "spacy":
            self.backend = self._load_spacy_backend()
        elif backend == "scispacy":
            self.backend = self._load_scispacy_backend()
        else:
            raise ValueError(f"Backend '{backend}' not implemented")
        
        logger.info(f"Initialized NER Tool with backend '{backend}'")
    
    def _load_spacy_backend(self):
        """
        Load the spaCy NER backend.
        
        Returns:
            NERBackend: The spaCy NER backend
        
        Raises:
            ImportError: If spaCy is not installed
        """
        try:
            from .backends.spacy_backend import SpacyNERBackend
            return SpacyNERBackend()
        except ImportError:
            msg = (
                "spaCy is not installed. Install it with: pip install spacy\n"
                "Then download a model with: python -m spacy download en_core_web_sm"
            )
            logger.error(msg)
            raise ImportError(msg)
    
    def _load_scispacy_backend(self):
        """
        Load the scispaCy NER backend.
        
        Returns:
            NERBackend: The scispaCy NER backend
        
        Raises:
            ImportError: If scispaCy is not installed
        """
        try:
            from .backends.scispacy_backend import ScispacyNERBackend
            return ScispacyNERBackend()
        except ImportError:
            msg = (
                "scispaCy is not installed. Install it with: pip install spacy scispacy\n"
                "Then download a model with: pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_core_sci_sm-0.5.0.tar.gz"
            )
            logger.error(msg)
            raise ImportError(msg)
    
    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract entities from the given text using the selected backend.
        
        Args:
            text (str): Text to extract entities from
        
        Returns:
            List[Entity]: List of extracted entities
        """
        if not text or not text.strip():
            return []
        
        return self.backend.extract_entities(text)
    
    def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a document to extract entities from its text content.
        
        Args:
            document (Dict[str, Any]): Document with text content to process
                Expected format: {"id": str, "title": str, "abstract": str, ...}
        
        Returns:
            Dict[str, Any]: Document with added entities
        """
        processed_doc = document.copy()
        
        # Extract entities from title
        if "title" in document and document["title"]:
            title_entities = self.extract_entities(document["title"])
            processed_doc["title_entities"] = [entity.to_dict() for entity in title_entities]
        
        # Extract entities from abstract
        if "abstract" in document and document["abstract"]:
            abstract_entities = self.extract_entities(document["abstract"])
            processed_doc["abstract_entities"] = [entity.to_dict() for entity in abstract_entities]
        
        # Extract entities from full text if available
        if "full_text" in document and document["full_text"]:
            # For long texts, process in chunks to avoid memory issues
            if len(document["full_text"]) > 10000:
                chunks = self._split_text_into_chunks(document["full_text"], chunk_size=5000, overlap=200)
                full_text_entities = []
                
                for chunk in chunks:
                    chunk_entities = self.extract_entities(chunk["text"])
                    # Adjust start_char and end_char based on chunk offset
                    for entity in chunk_entities:
                        entity.start_char += chunk["offset"]
                        entity.end_char += chunk["offset"]
                    
                    full_text_entities.extend(chunk_entities)
            else:
                full_text_entities = self.extract_entities(document["full_text"])
            
            processed_doc["full_text_entities"] = [entity.to_dict() for entity in full_text_entities]
        
        return processed_doc
    
    def get_backend_info(self) -> Dict[str, Any]:
        """
        Get information about the currently loaded backend.
        
        Returns:
            Dict[str, Any]: Backend information
        """
        return self.backend_info
    
    def _split_text_into_chunks(
        self, text: str, chunk_size: int = 5000, overlap: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Split a long text into overlapping chunks for processing.
        
        Args:
            text (str): Text to split
            chunk_size (int): Maximum size of each chunk
            overlap (int): Number of characters to overlap between chunks
        
        Returns:
            List[Dict[str, Any]]: List of chunks with their offsets
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            
            # If this is not the last chunk, try to find a sentence boundary
            if end < len(text):
                # Look for a period followed by whitespace within the overlap region
                boundary = text.rfind(". ", end - overlap, end)
                if boundary != -1:
                    end = boundary + 1  # Include the period
            
            chunks.append({
                "text": text[start:end],
                "offset": start
            })
            
            # Move start position, accounting for overlap
            if end == len(text):
                break
            
            start = end - overlap
        
        return chunks
    
    @staticmethod
    def list_available_backends() -> Dict[str, Dict[str, Any]]:
        """
        List all available NER backends with their details.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of available backends
        """
        return NER_BACKENDS
    
    @staticmethod
    def check_backend_availability(backend_name: str) -> Tuple[bool, str]:
        """
        Check if a backend is available (installed and ready to use).
        
        Args:
            backend_name (str): Name of the backend to check
        
        Returns:
            Tuple[bool, str]: (is_available, message)
            
        Raises:
            ValueError: If the specified backend is not supported
        """
        if backend_name not in NER_BACKENDS:
            raise ValueError(f"Backend '{backend_name}' not supported")
            
        if backend_name == "dummy":
            return True, "Dummy backend is always available"
        
        if backend_name == "spacy":
            try:
                import spacy
                return True, f"spaCy {spacy.__version__} is installed"
            except ImportError:
                return False, "spaCy is not installed"
        
        if backend_name == "scispacy":
            try:
                import spacy
                import scispacy
                return True, f"spaCy {spacy.__version__} and scispaCy {scispacy.__version__} are installed"
            except ImportError as e:
                return False, f"Required package not installed: {str(e)}"
        
        return False, f"Unknown backend: {backend_name}"
