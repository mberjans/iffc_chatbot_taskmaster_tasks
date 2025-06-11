"""
scispaCy backend implementation for the NER tool.

This module provides a NER backend using scispaCy biomedical models.
"""

from typing import List, Dict, Any
import logging

from ..ner_tool import NERBackend, Entity
from ..entities import BIOMEDICAL_ENTITY_TYPES

# Configure logging
logger = logging.getLogger(__name__)

class ScispacyNERBackend(NERBackend):
    """
    NER backend using scispaCy biomedical models.
    """
    
    def __init__(self, model_name: str = "en_core_sci_sm"):
        """
        Initialize the scispaCy NER backend.
        
        Args:
            model_name (str): Name of the scispaCy model to use
        
        Raises:
            ImportError: If scispaCy or the model is not installed
        """
        try:
            import spacy
            import scispacy
            
            try:
                self.nlp = spacy.load(model_name)
                self.model_name = model_name
                logger.info(f"Loaded scispaCy model: {model_name}")
            except OSError:
                logger.error(f"scispaCy model '{model_name}' is not installed")
                raise ImportError(
                    f"scispaCy model '{model_name}' is not installed. "
                    f"Install it with: pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/{model_name}-0.5.0.tar.gz"
                )
        except ImportError as e:
            logger.error(f"Required package not installed: {str(e)}")
            raise ImportError(
                "scispaCy is not installed. Install it with: pip install spacy scispacy"
            )
        
        # Map scispaCy entity labels to our standardized types
        self._entity_mapping = self._create_entity_mapping()
    
    def _create_entity_mapping(self) -> Dict[str, str]:
        """
        Create a mapping from scispaCy entity labels to our standardized types.
        
        Returns:
            Dict[str, str]: Mapping from scispaCy entity labels to standardized types
        """
        # This is a mapping from common scispaCy entity labels to our standardized types
        mapping = {
            "GENE": "GENE",
            "GENE_OR_GENE_PRODUCT": "GENE",
            "CHEMICAL": "CHEMICAL",
            "DISEASE": "DISEASE",
            "CELL_TYPE": "CELL_TYPE",
            "CELL_LINE": "CELL_LINE",
            "ORGANISM": "SPECIES",
            "SPECIES": "SPECIES",
            "MUTATION": "MUTATION",
            "DRUG": "DRUG",
            "ANATOMICAL_STRUCTURE": "ANATOMY",
            "BIOLOGICAL_PROCESS": "BIOLOGICAL_PROCESS",
            "MOLECULAR_FUNCTION": "MOLECULAR_FUNCTION",
            "PATHWAY": "PATHWAY"
            # Add more mappings as needed
        }
        
        return mapping
    
    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract entities from the given text using scispaCy.
        
        Args:
            text (str): Text to extract entities from
            
        Returns:
            List[Entity]: List of extracted entities
        """
        if not text or not text.strip():
            return []
        
        # Process the text with scispaCy
        doc = self.nlp(text)
        
        # Extract entities
        entities = []
        
        # Get all the entities
        for ent in doc.ents:
            entity_type = self._entity_mapping.get(ent.label_, ent.label_)
            
            # Only include entity types that we've defined
            if entity_type in BIOMEDICAL_ENTITY_TYPES:
                entity = Entity(
                    text=ent.text,
                    entity_type=entity_type,
                    start_char=ent.start_char,
                    end_char=ent.end_char,
                    source_text=text
                )
                entities.append(entity)
        
        return entities
    
    @property
    def supported_entity_types(self) -> List[str]:
        """
        Get the list of entity types supported by this backend.
        
        Returns:
            List[str]: List of supported entity types
        """
        # Return the biomedical entity types that this backend can detect
        return [
            entity_type for entity_type in BIOMEDICAL_ENTITY_TYPES.keys()
            if entity_type in set(self._entity_mapping.values())
        ]
    
    @property
    def backend_name(self) -> str:
        """
        Get the name of this backend.
        
        Returns:
            str: Name of the backend
        """
        return "scispacy"
