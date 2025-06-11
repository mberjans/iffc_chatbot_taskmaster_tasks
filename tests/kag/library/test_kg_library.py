"""
Tests for the Knowledge Graph Library module.

This module contains unit tests for the KG library selection and utility functions.
"""

import unittest
import sys
import os
import tempfile

# Add the src directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.kag.library import (
    KG_LIBRARY,
    create_knowledge_graph,
    add_entity,
    add_relation,
    get_entity,
    get_relations,
    get_entities_by_type,
    serialize_graph,
    deserialize_graph,
    save_graph,
    load_graph,
    get_library_info
)

def test_kg_library_defined():
    """Test that the KG library is properly defined."""
    assert KG_LIBRARY is not None, "KG_LIBRARY should be defined"
    assert "name" in KG_LIBRARY, "KG_LIBRARY should have a name"
    assert KG_LIBRARY["name"] == "NetworkX", "Selected library should be NetworkX"

def test_create_knowledge_graph():
    """Test creating a new knowledge graph."""
    graph = create_knowledge_graph()
    assert graph is not None, "Should create a non-None graph"
    assert len(graph.nodes) == 0, "New graph should have no nodes"
    assert len(graph.edges) == 0, "New graph should have no edges"

def test_add_entity():
    """Test adding an entity to the graph."""
    graph = create_knowledge_graph()
    
    # Add a paper entity
    paper_properties = {
        "paper_id": "paper123",
        "title": "Test Paper",
        "abstract": "This is a test abstract",
        "doi": "10.1234/test",
        "pmid": "12345678",
        "journal": "Test Journal",
        "publish_date": "2023-01-01",
        "url": "https://example.com/paper123"
    }
    
    add_entity(graph, "paper123", "Paper", paper_properties)
    
    assert len(graph.nodes) == 1, "Graph should have one node"
    assert "paper123" in graph.nodes, "Node with ID 'paper123' should exist"
    assert graph.nodes["paper123"]["entity_type"] == "Paper", "Node should have entity_type 'Paper'"
    assert graph.nodes["paper123"]["title"] == "Test Paper", "Node should have title property"

def test_add_relation():
    """Test adding a relation between entities."""
    graph = create_knowledge_graph()
    
    # Add paper and author entities
    add_entity(graph, "paper123", "Paper", {"title": "Test Paper"})
    add_entity(graph, "author456", "Author", {"name": "Test Author"})
    
    # Add relation
    add_relation(graph, "paper123", "author456", "AUTHORED_BY", {"order": 1})
    
    assert len(graph.edges) == 1, "Graph should have one edge"
    assert graph.has_edge("paper123", "author456"), "Edge should exist between paper and author"
    
    # Get edge data
    edge_data = graph.get_edge_data("paper123", "author456")[0]  # Get first edge data
    assert edge_data["relation_type"] == "AUTHORED_BY", "Edge should have relation_type 'AUTHORED_BY'"
    assert edge_data["order"] == 1, "Edge should have order property"

def test_get_entity():
    """Test getting an entity from the graph."""
    graph = create_knowledge_graph()
    
    # Add a paper entity
    paper_properties = {
        "paper_id": "paper123",
        "title": "Test Paper"
    }
    
    add_entity(graph, "paper123", "Paper", paper_properties)
    
    # Get entity
    entity = get_entity(graph, "paper123")
    
    assert entity is not None, "Should return entity data"
    assert entity["entity_type"] == "Paper", "Entity should have correct type"
    assert entity["title"] == "Test Paper", "Entity should have correct properties"
    
    # Test non-existent entity
    try:
        get_entity(graph, "nonexistent")
        assert False, "Should raise ValueError for non-existent entity"
    except ValueError:
        pass

def test_get_relations():
    """Test getting relations from the graph."""
    graph = create_knowledge_graph()
    
    # Add entities
    add_entity(graph, "paper1", "Paper", {"title": "Paper 1"})
    add_entity(graph, "paper2", "Paper", {"title": "Paper 2"})
    add_entity(graph, "author1", "Author", {"name": "Author 1"})
    add_entity(graph, "author2", "Author", {"name": "Author 2"})
    
    # Add relations
    add_relation(graph, "paper1", "author1", "AUTHORED_BY", {"order": 1})
    add_relation(graph, "paper1", "author2", "AUTHORED_BY", {"order": 2})
    add_relation(graph, "paper2", "author1", "AUTHORED_BY", {"order": 1})
    add_relation(graph, "paper1", "paper2", "CITES", {"context": "Introduction"})
    
    # Test getting all relations
    all_relations = get_relations(graph)
    assert len(all_relations) == 4, "Should return all relations"
    
    # Test filtering by source
    paper1_relations = get_relations(graph, source_id="paper1")
    assert len(paper1_relations) == 3, "Should return relations from paper1"
    
    # Test filtering by target
    author1_relations = get_relations(graph, target_id="author1")
    assert len(author1_relations) == 2, "Should return relations to author1"
    
    # Test filtering by relation type
    authored_relations = get_relations(graph, relation_type="AUTHORED_BY")
    assert len(authored_relations) == 3, "Should return AUTHORED_BY relations"
    
    # Test combined filtering
    paper1_authored_relations = get_relations(graph, source_id="paper1", relation_type="AUTHORED_BY")
    assert len(paper1_authored_relations) == 2, "Should return AUTHORED_BY relations from paper1"

def test_get_entities_by_type():
    """Test getting entities by type."""
    graph = create_knowledge_graph()
    
    # Add entities of different types
    add_entity(graph, "paper1", "Paper", {"title": "Paper 1"})
    add_entity(graph, "paper2", "Paper", {"title": "Paper 2"})
    add_entity(graph, "author1", "Author", {"name": "Author 1"})
    add_entity(graph, "author2", "Author", {"name": "Author 2"})
    add_entity(graph, "gene1", "Gene", {"symbol": "BRCA1"})
    
    # Get papers
    papers = get_entities_by_type(graph, "Paper")
    assert len(papers) == 2, "Should return 2 papers"
    paper_ids = [p[0] for p in papers]
    assert "paper1" in paper_ids, "Should include paper1"
    assert "paper2" in paper_ids, "Should include paper2"
    
    # Get authors
    authors = get_entities_by_type(graph, "Author")
    assert len(authors) == 2, "Should return 2 authors"
    
    # Get genes
    genes = get_entities_by_type(graph, "Gene")
    assert len(genes) == 1, "Should return 1 gene"
    assert genes[0][0] == "gene1", "Should be gene1"
    assert genes[0][1]["symbol"] == "BRCA1", "Should have correct symbol"

def test_serialize_deserialize_graph():
    """Test serializing and deserializing a graph."""
    # Create a test graph
    graph = create_knowledge_graph()
    add_entity(graph, "paper1", "Paper", {"title": "Paper 1"})
    add_entity(graph, "author1", "Author", {"name": "Author 1"})
    add_relation(graph, "paper1", "author1", "AUTHORED_BY", {"order": 1})
    
    # Test GraphML format
    graphml_data = serialize_graph(graph, format='graphml')
    assert graphml_data is not None, "Should return serialized data"
    assert len(graphml_data) > 0, "Serialized data should not be empty"
    
    # Deserialize and verify
    deserialized_graph = deserialize_graph(graphml_data, format='graphml')
    assert len(deserialized_graph.nodes) == 2, "Deserialized graph should have 2 nodes"
    assert len(deserialized_graph.edges) == 1, "Deserialized graph should have 1 edge"
    
    # Test JSON format
    json_data = serialize_graph(graph, format='json')
    assert json_data is not None, "Should return serialized data"
    assert len(json_data) > 0, "Serialized data should not be empty"
    
    # Deserialize and verify
    deserialized_graph = deserialize_graph(json_data, format='json')
    assert len(deserialized_graph.nodes) == 2, "Deserialized graph should have 2 nodes"
    assert len(deserialized_graph.edges) == 1, "Deserialized graph should have 1 edge"

def test_save_load_graph():
    """Test saving and loading a graph to/from a file."""
    # Create a test graph
    graph = create_knowledge_graph()
    add_entity(graph, "paper1", "Paper", {"title": "Paper 1"})
    add_entity(graph, "author1", "Author", {"name": "Author 1"})
    add_relation(graph, "paper1", "author1", "AUTHORED_BY", {"order": 1})
    
    # Create temporary files for testing
    with tempfile.NamedTemporaryFile(suffix='.graphml') as graphml_file, \
         tempfile.NamedTemporaryFile(suffix='.json') as json_file:
        
        # Test GraphML format
        save_graph(graph, graphml_file.name, format='graphml')
        loaded_graph = load_graph(graphml_file.name, format='graphml')
        
        assert len(loaded_graph.nodes) == 2, "Loaded graph should have 2 nodes"
        assert len(loaded_graph.edges) == 1, "Loaded graph should have 1 edge"
        
        # Test JSON format
        save_graph(graph, json_file.name, format='json')
        loaded_graph = load_graph(json_file.name, format='json')
        
        assert len(loaded_graph.nodes) == 2, "Loaded graph should have 2 nodes"
        assert len(loaded_graph.edges) == 1, "Loaded graph should have 1 edge"

def test_get_library_info():
    """Test getting library information."""
    info = get_library_info()
    assert info is not None, "Should return library info"
    assert info == KG_LIBRARY, "Should return the KG_LIBRARY dictionary"
    assert "name" in info, "Info should include library name"
    assert "selection_rationale" in info, "Info should include selection rationale"
    assert "limitations" in info, "Info should include limitations"
    assert "future_alternatives" in info, "Info should include future alternatives"

def run_all_tests():
    """Run all test functions."""
    test_functions = [
        test_kg_library_defined,
        test_create_knowledge_graph,
        test_add_entity,
        test_add_relation,
        test_get_entity,
        test_get_relations,
        test_get_entities_by_type,
        test_serialize_deserialize_graph,
        test_save_load_graph,
        test_get_library_info
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
