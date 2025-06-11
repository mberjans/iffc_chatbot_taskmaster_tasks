"""
spaCy backend implementation for the NER tool.

This module provides a NER backend using spaCy models.
"""

from typing import List, Dict, Any
import logging

from ..ner_tool import NERBackend, Entity

# Configure logging
logger = logging.getLogger(__name__)

class SpacyNERBackend(NERBackend):
    """
    NER backend using spaCy models.
    """
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize the spaCy NER backend.
        
        Args:
            model_name (str): Name of the spaCy model to use
        
        Raises:
            ImportError: If spaCy or the model is not installed
        """
        try:
            import spacy
            self.nlp = spacy.load(model_name)
            self.model_name = model_name
            logger.info(f"Loaded spaCy model: {model_name}")
        except ImportError:
            logger.error("spaCy is not installed")
            raise ImportError("spaCy is not installed. Install it with: pip install spacy")
        except OSError:
            logger.error(f"spaCy model '{model_name}' is not installed")
            raise ImportError(
                f"spaCy model '{model_name}' is not installed. "
                f"Install it with: python -m spacy download {model_name}"
            )
        
        # Map spaCy entity labels to our standardized types
        self._entity_mapping = self._create_entity_mapping()
    
    def _create_entity_mapping(self) -> Dict[str, str]:
        """
        Create a mapping from spaCy entity labels to our standardized types.
        
        Returns:
            Dict[str, str]: Mapping from spaCy entity labels to standardized types
        """
        # This is a simplified mapping, in a real implementation this would be more comprehensive
        mapping = {
            "PERSON": "PERSON",
            "ORG": "ORGANIZATION",
            "GPE": "LOCATION",
            "LOC": "LOCATION",
            "PRODUCT": "PRODUCT",
            "DISEASE": "DISEASE",
            "CHEMICAL": "CHEMICAL"
            # Add more mappings as needed
        }
        
        return mapping
    
    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract entities from the given text using spaCy.
        
        Args:
            text (str): Text to extract entities from
            
        Returns:
            List[Entity]: List of extracted entities
        """
        if not text or not text.strip():
            return []
        
        # Process the text with spaCy
        doc = self.nlp(text)
        
        # Extract entities
        entities = []
        
        # Get all the entities
        doc_entities = doc.ents
        for i in range(len(doc_entities)):
            ent = doc_entities[i]
            entity_type = self._entity_mapping.get(ent.label_, ent.label_)
            
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
        # Get the entity types from the spaCy pipeline
        entity_types = []
        
        # Add entity types from the mapping
        for spacy_type, our_type in self._entity_mapping.items():
            if our_type not in entity_types:
                entity_types.append(our_type)
        
        return entity_types
    
    @property
    def backend_name(self) -> str:
        """
        Get the name of this backend.
        
        Returns:
            str: Name of the backend
        """
        return "spacy"
