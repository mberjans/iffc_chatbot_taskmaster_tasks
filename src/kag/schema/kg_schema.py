"""
Knowledge Graph Schema Definition for Knowledge Augmented Generation (KAG) Module.

This module defines the schema for the Knowledge Graph (KG) used in the KAG module.
The schema includes entity types, relation types, and their properties that will be 
extracted from PubMed XML documents.
"""

# Dictionary of entity types and their properties
ENTITY_TYPES = {
    "Paper": {
        "description": "A scientific paper or article",
        "properties": {
            "paper_id": str,
            "title": str,
            "abstract": str,
            "doi": str,
            "pmid": str,
            "journal": str,
            "publish_date": str,
            "url": str,
        }
    },
    "Author": {
        "description": "An author of a scientific paper",
        "properties": {
            "name": str,
            "affiliation": str,
            "email": str,
            "orcid": str
        }
    },
    "Section": {
        "description": "A section within a paper",
        "properties": {
            "section_id": str,
            "title": str,
            "text": str,
            "position": int
        }
    },
    "Figure": {
        "description": "A figure within a paper",
        "properties": {
            "figure_id": str,
            "caption": str,
            "reference": str
        }
    },
    "Table": {
        "description": "A table within a paper",
        "properties": {
            "table_id": str,
            "caption": str,
            "reference": str,
            "data": str  # Serialized representation of table data
        }
    },
    "Citation": {
        "description": "A citation or reference",
        "properties": {
            "citation_id": str,
            "text": str,
            "doi": str,
            "pmid": str
        }
    },
    "Concept": {
        "description": "A scientific concept or term",
        "properties": {
            "name": str,
            "definition": str,
            "category": str
        }
    },
    "Method": {
        "description": "A research method or protocol",
        "properties": {
            "name": str,
            "description": str,
            "parameters": str
        }
    },
    "Result": {
        "description": "An experimental result or finding",
        "properties": {
            "description": str,
            "value": str,
            "unit": str,
            "confidence": float,
            "p_value": float
        }
    },
    "Gene": {
        "description": "A gene entity",
        "properties": {
            "symbol": str,
            "full_name": str,
            "gene_id": str,
            "organism": str
        }
    },
    "Protein": {
        "description": "A protein entity",
        "properties": {
            "name": str,
            "uniprot_id": str,
            "sequence": str,
            "function": str
        }
    },
    "Disease": {
        "description": "A disease or medical condition",
        "properties": {
            "name": str,
            "mesh_id": str,
            "synonyms": str,  # Comma-separated list
            "definition": str
        }
    },
    "Chemical": {
        "description": "A chemical compound or substance",
        "properties": {
            "name": str,
            "formula": str,
            "cas_number": str,
            "mesh_id": str,
            "smiles": str
        }
    }
}

# Dictionary of relation types between entities
RELATION_TYPES = {
    "AUTHORED_BY": {
        "description": "Connects a Paper to its Authors",
        "source": ["Paper"],
        "target": ["Author"],
        "properties": {
            "contribution": str,
            "order": int
        }
    },
    "CONTAINS_SECTION": {
        "description": "Connects a Paper to its Sections",
        "source": ["Paper"],
        "target": ["Section"],
        "properties": {
            "section_type": str,  # e.g., 'introduction', 'methods', 'results', 'discussion'
        }
    },
    "CONTAINS_FIGURE": {
        "description": "Connects a Paper or Section to its Figures",
        "source": ["Paper", "Section"],
        "target": ["Figure"],
        "properties": {}
    },
    "CONTAINS_TABLE": {
        "description": "Connects a Paper or Section to its Tables",
        "source": ["Paper", "Section"],
        "target": ["Table"],
        "properties": {}
    },
    "CITES": {
        "description": "Connects a Paper to its Citations",
        "source": ["Paper", "Section"],
        "target": ["Citation"],
        "properties": {
            "context": str
        }
    },
    "MENTIONS": {
        "description": "Connects a Section to the Concepts it mentions",
        "source": ["Section", "Figure", "Table"],
        "target": ["Concept", "Gene", "Protein", "Disease", "Chemical", "Method", "Result"],
        "properties": {
            "count": int,
            "context": str
        }
    },
    "INTERACTS_WITH": {
        "description": "Describes interaction between biological entities",
        "source": ["Gene", "Protein"],
        "target": ["Gene", "Protein"],
        "properties": {
            "interaction_type": str,
            "confidence": float,
            "evidence": str
        }
    },
    "ASSOCIATES_WITH": {
        "description": "Describes association between biomedical entities",
        "source": ["Gene", "Protein", "Chemical"],
        "target": ["Disease", "Concept"],
        "properties": {
            "association_type": str,
            "strength": float,
            "evidence": str
        }
    },
    "USED_IN": {
        "description": "Describes a method used in a section",
        "source": ["Method"],
        "target": ["Section", "Result"],
        "properties": {
            "context": str
        }
    },
    "RESULTS_IN": {
        "description": "Connects a method to its results",
        "source": ["Method"],
        "target": ["Result"],
        "properties": {
            "context": str
        }
    },
    "SUPPORTS": {
        "description": "Indicates a result supports a concept/finding",
        "source": ["Result"],
        "target": ["Concept"],
        "properties": {
            "strength": float,
            "context": str
        }
    },
    "CONTRADICTS": {
        "description": "Indicates a result contradicts a concept/finding",
        "source": ["Result"],
        "target": ["Concept"],
        "properties": {
            "strength": float,
            "context": str
        }
    }
}

# Schema validation functions 
def validate_entity(entity_type, entity_data):
    """
    Validate an entity against the schema.
    
    Args:
        entity_type (str): Type of the entity as defined in ENTITY_TYPES
        entity_data (dict): Data for the entity to validate
        
    Returns:
        bool: True if entity is valid, False otherwise
        
    Raises:
        ValueError: If entity_type is not defined in the schema
    """
    if entity_type not in ENTITY_TYPES:
        raise ValueError(f"Entity type '{entity_type}' not defined in schema")
    
    entity_schema = ENTITY_TYPES[entity_type]["properties"]
    
    # Check required properties
    for prop, prop_type in entity_schema.items():
        if prop not in entity_data:
            return False
        if entity_data[prop] is not None and not isinstance(entity_data[prop], prop_type):
            return False
            
    return True

def validate_relation(relation_type, source_type, target_type, relation_data):
    """
    Validate a relation against the schema.
    
    Args:
        relation_type (str): Type of the relation as defined in RELATION_TYPES
        source_type (str): Type of the source entity
        target_type (str): Type of the target entity
        relation_data (dict): Data for the relation to validate
        
    Returns:
        bool: True if relation is valid, False otherwise
        
    Raises:
        ValueError: If relation_type is not defined in the schema
    """
    if relation_type not in RELATION_TYPES:
        raise ValueError(f"Relation type '{relation_type}' not defined in schema")
        
    relation_schema = RELATION_TYPES[relation_type]
    
    # Check source and target entity types
    if source_type not in relation_schema["source"]:
        return False
    if target_type not in relation_schema["target"]:
        return False
        
    # Check properties
    for prop, prop_type in relation_schema.get("properties", {}).items():
        if prop in relation_data and relation_data[prop] is not None:
            if not isinstance(relation_data[prop], prop_type):
                return False
                
    return True

def get_entity_types():
    """
    Get the list of all defined entity types.
    
    Returns:
        list: List of entity type names
    """
    return list(ENTITY_TYPES.keys())

def get_relation_types():
    """
    Get the list of all defined relation types.
    
    Returns:
        list: List of relation type names
    """
    return list(RELATION_TYPES.keys())

def get_entity_schema(entity_type):
    """
    Get the schema for a specific entity type.
    
    Args:
        entity_type (str): The entity type to get schema for
        
    Returns:
        dict: The entity schema
        
    Raises:
        ValueError: If entity_type is not defined in the schema
    """
    if entity_type not in ENTITY_TYPES:
        raise ValueError(f"Entity type '{entity_type}' not defined in schema")
        
    return ENTITY_TYPES[entity_type]

def get_relation_schema(relation_type):
    """
    Get the schema for a specific relation type.
    
    Args:
        relation_type (str): The relation type to get schema for
        
    Returns:
        dict: The relation schema
        
    Raises:
        ValueError: If relation_type is not defined in the schema
    """
    if relation_type not in RELATION_TYPES:
        raise ValueError(f"Relation type '{relation_type}' not defined in schema")
        
    return RELATION_TYPES[relation_type]
