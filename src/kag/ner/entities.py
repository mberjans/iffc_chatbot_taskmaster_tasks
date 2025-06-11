"""
Entity types and constants for the Named Entity Recognition (NER) tool.

This module defines the common entity types and constants used in biomedical NER.
"""

# Define entity types of interest for biomedical NER
BIOMEDICAL_ENTITY_TYPES = {
    "GENE": "Gene or gene product",
    "PROTEIN": "Protein",
    "DISEASE": "Disease or syndrome",
    "CHEMICAL": "Chemical compound",
    "SPECIES": "Species or organism",
    "MUTATION": "Genetic mutation",
    "PATHWAY": "Biological pathway",
    "CELL_TYPE": "Cell type",
    "CELL_LINE": "Cell line",
    "DRUG": "Drug or medication",
    "ANATOMY": "Anatomical structure",
    "BIOLOGICAL_PROCESS": "Biological process",
    "MOLECULAR_FUNCTION": "Molecular function"
}

# Define available NER model backends
NER_BACKENDS = {
    "dummy": {
        "name": "Dummy NER",
        "description": "Simple pattern-based NER for demonstration purposes",
        "requires_install": False,
        "languages": ["en"],
        "entity_types": list(BIOMEDICAL_ENTITY_TYPES.keys())
    },
    "spacy": {
        "name": "spaCy NER",
        "description": "NER using spaCy models",
        "requires_install": True,
        "languages": ["en"],
        "installation": "pip install spacy",
        "entity_types": list(BIOMEDICAL_ENTITY_TYPES.keys())
    },
    "scispacy": {
        "name": "SciSpaCy NER",
        "description": "Biomedical NER using scispaCy models",
        "requires_install": True,
        "languages": ["en"],
        "installation": "pip install spacy scispacy",
        "models": {
            "en_core_sci_sm": "Small English biomedical model",
            "en_core_sci_md": "Medium English biomedical model",
            "en_ner_bc5cdr_md": "NER model trained on BC5CDR corpus",
            "en_ner_bionlp13cg_md": "NER model trained on BIONLP13CG corpus"
        },
        "entity_types": list(BIOMEDICAL_ENTITY_TYPES.keys())
    }
}
