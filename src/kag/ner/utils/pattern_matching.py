"""
Pattern matching utilities for biomedical named entity recognition.

This module provides functions for pattern-based entity extraction in biomedical text
without using regular expressions.
"""

from typing import Dict, List, Tuple, Optional, Any, Set, Callable

def create_pattern(pattern_string: str, case_insensitive: bool = True) -> Pattern:
    """
    Create a compiled regular expression pattern.
    
    Args:
        pattern_string (str): The regular expression pattern string
        case_insensitive (bool): Whether to make the pattern case insensitive
        
    Returns:
        Pattern: Compiled regular expression pattern
    """
    flags = re.IGNORECASE if case_insensitive else 0
    return re.compile(pattern_string, flags)

def find_matches(text: str, pattern: Pattern) -> List[Tuple[int, int, str]]:
    """
    Find all matches of a pattern in text.
    
    Args:
        text (str): Text to search in
        pattern (Pattern): Compiled regular expression pattern
        
    Returns:
        List[Tuple[int, int, str]]: List of (start_pos, end_pos, matched_text) tuples
    """
    if not text:
        return []
    
    matches = []
    for match in pattern.finditer(text):
        start, end = match.span()
        matched_text = match.group()
        matches.append((start, end, matched_text))
    
    return matches

def get_biomedical_patterns() -> Dict[str, str]:
    """
    Get a dictionary of pattern strings for biomedical entity types.
    
    Returns:
        Dict[str, str]: Dictionary mapping entity types to pattern strings
    """
    patterns = {
        # Gene patterns - capture gene symbols like BRCA1, TP53, etc.
        "GENE": r'\b[A-Z][A-Z0-9-]{1,8}[0-9]?\b|\b[A-Z][a-z]{1,8}[0-9]+\b',
        
        # Protein patterns - similar to genes but can include more complex names with dashes
        "PROTEIN": r'\b[A-Z][A-Z0-9-]{1,10}\b|\b[A-Z][a-z]{2,10}(in|ase|or)\b',
        
        # Disease patterns - common disease terms and patterns
        "DISEASE": r'\b(cancer|carcinoma|tumor|disease|syndrome|disorder|infection|fibrosis|dystrophy|deficiency|arthritis|diabetes|sclerosis|anemia|leukemia)\b',
        
        # Chemical compound patterns
        "CHEMICAL": r'\b[A-Z][a-z]*(?:acid|ine|ol|ate|ide|ium|gen|ane|ene|one|ase|yl|ic|al)\b',
        
        # Species/Organism patterns
        "SPECIES": r'\b[A-Z][a-z]+ [a-z]+\b|\bE\. coli\b|\bS\. aureus\b|\bC\. elegans\b|\bD\. melanogaster\b',
        
        # Mutation patterns - e.g., G12D, p.V600E
        "MUTATION": r'\b[A-Z][0-9]+[A-Z]\b|\bp\.[A-Z][0-9]+[A-Z]\b|\bc\.[0-9]+[A-Z]>[A-Z]\b',
        
        # Biological pathway patterns
        "PATHWAY": r'\b[A-Z][A-Z0-9-]{1,10} (pathway|signaling|cascade|cycle)\b',
        
        # Cell type patterns
        "CELL_TYPE": r'\b(T cell|B cell|NK cell|stem cell|neuron|fibroblast|macrophage|monocyte|lymphocyte|erythrocyte|platelet)\b',
        
        # Cell line patterns - common formats for cell lines
        "CELL_LINE": r'\b[A-Z]-?[0-9]+\b|\b[A-Z]{2,5}-[0-9]+\b|\bHEK-?293\b|\bHeLa\b|\bMCF-?7\b',
        
        # Drug patterns
        "DRUG": r'\b[A-Z][a-z]{2,20}(?:mab|nib|zumab|ximab|lin|dipine|statin|sartan|prazole|pril|oxacin|mycin)\b',
        
        # Anatomy patterns
        "ANATOMY": r'\b(brain|heart|lung|liver|kidney|muscle|bone|blood|skin|nerve|artery|vein|intestine|pancreas|spleen)\b',
        
        # Biological process patterns
        "BIOLOGICAL_PROCESS": r'\b(apoptosis|proliferation|differentiation|transcription|translation|metabolism|replication|autophagy|angiogenesis)\b',
        
        # Molecular function patterns
        "MOLECULAR_FUNCTION": r'\b(binding|catalysis|transport|regulation|inhibition|activation|phosphorylation|methylation|ubiquitination)\b'
    }
    
    return patterns

def extract_pattern_matches(text: str, patterns: Dict[str, str], case_insensitive: bool = True) -> Dict[str, List[Tuple[int, int, str]]]:
    """
    Extract matches for multiple patterns from text.
    
    Args:
        text (str): Text to search in
        patterns (Dict[str, str]): Dictionary mapping entity types to pattern strings
        case_insensitive (bool): Whether to make patterns case insensitive
        
    Returns:
        Dict[str, List[Tuple[int, int, str]]]: Dictionary mapping entity types to lists of matches
    """
    if not text or not text.strip():
        return {}
    
    results = {}
    
    # Compile patterns and find matches for each entity type
    for entity_type, pattern_string in patterns.items():
        pattern = create_pattern(pattern_string, case_insensitive)
        matches = find_matches(text, pattern)
        
        if matches:
            results[entity_type] = matches
    
    return results

def find_entity_mentions(text: str, entity_type: str = None) -> Dict[str, List[Tuple[int, int, str]]]:
    """
    Find mentions of biomedical entities in text.
    
    Args:
        text (str): Text to search for entity mentions
        entity_type (str, optional): Specific entity type to look for. If None, find all types.
        
    Returns:
        Dict[str, List[Tuple[int, int, str]]]: Dictionary mapping entity types to lists of matches
    """
    patterns = get_biomedical_patterns()
    
    if entity_type:
        if entity_type not in patterns:
            return {}
        
        # Extract matches for just the specific entity type
        pattern = create_pattern(patterns[entity_type])
        matches = find_matches(text, pattern)
        
        if matches:
            return {entity_type: matches}
        return {}
    
    # Extract matches for all entity types
    return extract_pattern_matches(text, patterns)
