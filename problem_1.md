# Problem: Python 3.13 Compatibility Issues with spaCy/scispaCy in NER Tool Implementation

## Background

The Nexus Scholar AI project requires a Named Entity Recognition (NER) tool for biomedical text processing as part of the Knowledge Augmented Generation (KAG) module. The original implementation used spaCy with scispaCy biomedical models, but we encountered compatibility issues with Python 3.13. Specifically, the `blis` package (a dependency of spaCy) fails to build on Python 3.13.

## Current Status

1. We've implemented a flexible NER tool architecture with:
   - A base `Entity` class to represent extracted entities
   - An abstract `NERBackend` interface for different NER implementations
   - A `DummyNERBackend` using simple pattern matching that works without external dependencies
   - Placeholder implementations for spaCy and scispaCy backends
   - Directory structure for backend implementations

2. The implementation is located in:
   - `src/kag/ner/ner_tool.py`: Core NER tool implementation
   - `src/kag/ner/entities.py`: Entity type definitions
   - `src/kag/ner/backends/`: Backend implementations
   - `src/kag/ner/__init__.py`: Package exports

3. This architecture allows us to:
   - Use the basic pattern-matching backend without requiring any dependencies
   - Add more sophisticated backends when compatibility issues are resolved
   - Extract entities from text and documents with the same API regardless of backend

## Problems to Fix

1. **Test Suite Update**:
   - The test file (`tests/kag/ner/test_ner_tool.py`) needs to be updated to test the new implementation.
   - Tests should focus on the `DummyNERBackend` and base `NERTool` so they can run without spaCy/scispaCy.
   - Mock or skip the tests for spaCy/scispaCy backends when those libraries aren't available.

2. **Requirements Update**:
   - Update `requirements.txt` to make spaCy and scispaCy optional dependencies.
   - Consider adding a separate `requirements-optional.txt` file.

3. **Documentation Updates**:
   - Update `progress.md` with information about the new architecture and implementation.
   - Mark the NER tool task as completed in `checklist.md`.

4. **Integration with KAG Module**:
   - Ensure the NER tool is properly integrated with the rest of the KAG module.
   - Update `src/kag/__init__.py` to expose the right components.

## Proposed Solutions

1. **Test Suite Update**:
   - Create unit tests for the `Entity` class, testing all its methods.
   - Create unit tests for the `DummyNERBackend`, verifying it can extract simple entities.
   - Test the `NERTool` class with the `DummyNERBackend`.
   - Create conditional tests for spaCy/scispaCy backends that skip when the libraries aren't available.
   - Use mocking to test the backend interface without requiring the actual libraries.

2. **Requirements Update**:
   - Create a `requirements-optional.txt` file with:
     ```
     spacy==3.7.2
     scispacy==0.5.3
     ```
   - Add a comment to `requirements.txt` indicating that spaCy and scispaCy are optional.

3. **Documentation Updates**:
   - Update `progress.md` with a detailed description of the new architecture.
   - Include information about the `DummyNERBackend` and how it enables functionality without dependencies.
   - Check off the NER tool task in `checklist.md`.
   - Document how to install and use the optional dependencies when needed.

4. **Integration and Future Work**:
   - Extend the `DummyNERBackend` with more sophisticated pattern matching for biomedical entities.
   - When Python 3.13 compatibility issues are resolved, update the spaCy/scispaCy backends.
   - Consider alternative NER backends for biomedical text (e.g., NLTK, Hugging Face Transformers).

## Code Examples to Help

### Example Unit Test for Entity Class

```python
def test_entity_initialization():
    """Test Entity initialization and properties."""
    text = "BRCA1"
    entity_type = "GENE"
    start_char = 10
    end_char = 15
    source_text = "The BRCA1 gene is associated with breast cancer."
    
    entity = Entity(text, entity_type, start_char, end_char, source_text)
    
    assert entity.text == text
    assert entity.entity_type == entity_type
    assert entity.start_char == start_char
    assert entity.end_char == end_char
    assert entity.source_text == source_text

def test_entity_context():
    """Test getting context around an entity."""
    source_text = "The BRCA1 gene is associated with breast cancer and ovarian cancer."
    entity = Entity("BRCA1", "GENE", 4, 9, source_text)
    
    # Test with default window
    context = entity.get_context()
    assert "The BRCA1 gene is associated with" in context
    
    # Test with custom window
    context = entity.get_context(10)
    assert "The BRCA1 gene" in context
    assert len(context) <= 21  # 10 chars before + entity (5 chars) + 10 chars after
```

### Example Test for DummyNERBackend

```python
def test_dummy_ner_backend():
    """Test the DummyNERBackend's entity extraction."""
    backend = DummyNERBackend()
    text = "BRCA1 is associated with breast cancer."
    
    entities = backend.extract_entities(text)
    
    # Verify that we found at least one entity
    assert len(entities) > 0
    
    # Check that we found a gene (BRCA1)
    gene_entities = [e for e in entities if e.entity_type == "GENE"]
    assert len(gene_entities) > 0
    assert "BRCA1" in [e.text for e in gene_entities]
    
    # Check that we found a disease (cancer)
    disease_entities = [e for e in entities if e.entity_type == "DISEASE"]
    assert len(disease_entities) > 0
    assert "cancer" in [e.text for e in disease_entities]
```

## Conclusion

This flexible architecture allows us to proceed with NER functionality despite the compatibility issues with Python 3.13. The `DummyNERBackend` provides basic functionality while more advanced backends can be added when the dependency issues are resolved. The goal is to have a working NER tool that can be easily extended and improved over time.
