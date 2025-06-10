"""
Tests for the Knowledge Graph Schema module.

This module contains unit tests for the KG schema definitions and validation functions.
"""

import unittest
import sys
import os

# Add the src directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.kag.schema import (
    ENTITY_TYPES,
    RELATION_TYPES,
    validate_entity,
    validate_relation,
    get_entity_types,
    get_relation_types,
    get_entity_schema,
    get_relation_schema
)

def test_entity_types_defined():
    """Test that entity types are properly defined."""
    assert len(ENTITY_TYPES) > 0, "Should have at least one entity type defined"
    assert "Paper" in ENTITY_TYPES, "Paper entity type should be defined"
    assert "Author" in ENTITY_TYPES, "Author entity type should be defined"

def test_relation_types_defined():
    """Test that relation types are properly defined."""
    assert len(RELATION_TYPES) > 0, "Should have at least one relation type defined"
    assert "AUTHORED_BY" in RELATION_TYPES, "AUTHORED_BY relation type should be defined"
    assert "CITES" in RELATION_TYPES, "CITES relation type should be defined"

def test_entity_schema_structure():
    """Test that entity schemas have the correct structure."""
    for entity_type, schema in ENTITY_TYPES.items():
        assert "description" in schema, f"Entity {entity_type} should have a description"
        assert "properties" in schema, f"Entity {entity_type} should have properties defined"
        assert len(schema["properties"]) > 0, f"Entity {entity_type} should have at least one property"

def test_relation_schema_structure():
    """Test that relation schemas have the correct structure."""
    for relation_type, schema in RELATION_TYPES.items():
        assert "description" in schema, f"Relation {relation_type} should have a description"
        assert "source" in schema, f"Relation {relation_type} should have source types"
        assert "target" in schema, f"Relation {relation_type} should have target types"
        assert len(schema["source"]) > 0, f"Relation {relation_type} should have at least one source type"
        assert len(schema["target"]) > 0, f"Relation {relation_type} should have at least one target type"

def test_validate_valid_entity():
    """Test validation of a valid entity."""
    paper_entity = {
        "paper_id": "paper123",
        "title": "Test Paper",
        "abstract": "This is a test abstract",
        "doi": "10.1234/test",
        "pmid": "12345678",
        "journal": "Test Journal",
        "publish_date": "2023-01-01",
        "url": "https://example.com/paper123"
    }
    
    assert validate_entity("Paper", paper_entity) == True, "Valid Paper entity should validate"

def test_validate_invalid_entity_missing_property():
    """Test validation of an entity with missing properties."""
    paper_entity = {
        "paper_id": "paper123",
        "title": "Test Paper",
        # Missing abstract and other properties
    }
    
    assert validate_entity("Paper", paper_entity) == False, "Invalid Paper entity should not validate"

def test_validate_invalid_entity_wrong_type():
    """Test validation of an entity with wrong property types."""
    paper_entity = {
        "paper_id": "paper123",
        "title": "Test Paper",
        "abstract": "This is a test abstract",
        "doi": "10.1234/test",
        "pmid": 12345678,  # Should be string, not int
        "journal": "Test Journal",
        "publish_date": "2023-01-01",
        "url": "https://example.com/paper123"
    }
    
    assert validate_entity("Paper", paper_entity) == False, "Entity with wrong property types should not validate"

def test_validate_nonexistent_entity_type():
    """Test validation with a non-existent entity type."""
    try:
        validate_entity("NonExistentType", {})
        assert False, "Should raise ValueError for non-existent entity type"
    except ValueError:
        pass

def test_validate_valid_relation():
    """Test validation of a valid relation."""
    relation_data = {
        "contribution": "First author",
        "order": 1
    }
    
    assert validate_relation("AUTHORED_BY", "Paper", "Author", relation_data) == True, "Valid relation should validate"

def test_validate_invalid_relation_source():
    """Test validation of a relation with invalid source type."""
    relation_data = {
        "contribution": "First author",
        "order": 1
    }
    
    assert validate_relation("AUTHORED_BY", "Disease", "Author", relation_data) == False, "Relation with invalid source should not validate"

def test_validate_invalid_relation_target():
    """Test validation of a relation with invalid target type."""
    relation_data = {
        "contribution": "First author",
        "order": 1
    }
    
    assert validate_relation("AUTHORED_BY", "Paper", "Disease", relation_data) == False, "Relation with invalid target should not validate"

def test_validate_nonexistent_relation_type():
    """Test validation with a non-existent relation type."""
    try:
        validate_relation("NON_EXISTENT_RELATION", "Paper", "Author", {})
        assert False, "Should raise ValueError for non-existent relation type"
    except ValueError:
        pass

def test_get_entity_types():
    """Test getting all entity types."""
    entity_types = get_entity_types()
    assert len(entity_types) > 0, "Should return at least one entity type"
    assert "Paper" in entity_types, "Paper type should be in the list"

def test_get_relation_types():
    """Test getting all relation types."""
    relation_types = get_relation_types()
    assert len(relation_types) > 0, "Should return at least one relation type"
    assert "AUTHORED_BY" in relation_types, "AUTHORED_BY should be in the list"

def test_get_entity_schema():
    """Test getting schema for a specific entity type."""
    schema = get_entity_schema("Paper")
    assert "description" in schema, "Should return schema with description"
    assert "properties" in schema, "Should return schema with properties"

def test_get_relation_schema():
    """Test getting schema for a specific relation type."""
    schema = get_relation_schema("AUTHORED_BY")
    assert "description" in schema, "Should return schema with description"
    assert "source" in schema, "Should return schema with source types"
    assert "target" in schema, "Should return schema with target types"

def run_all_tests():
    """Run all test functions."""
    test_functions = [
        test_entity_types_defined,
        test_relation_types_defined,
        test_entity_schema_structure,
        test_relation_schema_structure,
        test_validate_valid_entity,
        test_validate_invalid_entity_missing_property,
        test_validate_invalid_entity_wrong_type,
        test_validate_nonexistent_entity_type,
        test_validate_valid_relation,
        test_validate_invalid_relation_source,
        test_validate_invalid_relation_target,
        test_validate_nonexistent_relation_type,
        test_get_entity_types,
        test_get_relation_types,
        test_get_entity_schema,
        test_get_relation_schema
    ]
    
    results = {
        "passed": 0,
        "failed": 0,
        "failures": []
    }
    
    for test_func in test_functions:
        try:
            test_func()
            results["passed"] += 1
            print(f"✅ {test_func.__name__}")
        except AssertionError as e:
            results["failed"] += 1
            results["failures"].append((test_func.__name__, str(e)))
            print(f"❌ {test_func.__name__}: {e}")
        except Exception as e:
            results["failed"] += 1
            results["failures"].append((test_func.__name__, str(e)))
            print(f"❌ {test_func.__name__}: Unexpected error - {e}")
    
    print(f"\nTest Summary: {results['passed']} passed, {results['failed']} failed")
    
    if results["failed"] > 0:
        print("\nFailure details:")
        for name, error in results["failures"]:
            print(f"  {name}: {error}")
    
    return results["failed"] == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
