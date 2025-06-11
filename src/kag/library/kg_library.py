"""
Knowledge Graph Library Selection and Configuration for the KAG Module.

This module defines the library to be used for Knowledge Graph construction and
manipulation in the KAG module. It provides utility functions for creating,
manipulating, and querying knowledge graphs.
"""

import logging
import networkx as nx
from typing import Dict, Any, List, Tuple, Optional, Set, Union

# Configure logging
logger = logging.getLogger(__name__)

# Define the chosen KG library and its configuration
KG_LIBRARY = {
    "name": "NetworkX",
    "version": nx.__version__,
    "description": "NetworkX is a Python package for the creation, manipulation, and study of the structure, "
                  "dynamics, and functions of complex networks.",
    "website": "https://networkx.org/",
    "github": "https://github.com/networkx/networkx",
    "documentation": "https://networkx.org/documentation/stable/",
    "selection_rationale": [
        "Pure Python implementation with minimal dependencies",
        "Strong support for graph algorithms and analysis",
        "Flexible data structures for representing entities and relationships",
        "In-memory representation suitable for Phase 1 requirements",
        "Extensive documentation and community support",
        "Easy integration with other Python libraries",
        "Straightforward serialization to disk formats",
        "Compatible with our defined KG schema"
    ],
    "limitations": [
        "Limited scalability for very large graphs (millions of nodes/edges)",
        "No built-in persistence layer",
        "Basic visualization capabilities (requires additional libraries)"
    ],
    "future_alternatives": [
        {
            "name": "Neo4j",
            "when_to_consider": "When graph size exceeds memory capacity or requires persistent storage",
            "benefits": [
                "Dedicated graph database with ACID compliance",
                "Cypher query language optimized for graph traversals",
                "Built-in visualization tools",
                "Horizontal scalability"
            ]
        }
    ]
}

def create_knowledge_graph() -> nx.MultiDiGraph:
    """
    Create a new empty knowledge graph.
    
    Returns:
        nx.MultiDiGraph: A new empty directed multigraph
    """
    # Using MultiDiGraph to allow multiple directed edges between the same nodes
    # This is useful for representing different types of relationships between the same entities
    return nx.MultiDiGraph()

def add_entity(graph: nx.MultiDiGraph, entity_id: str, entity_type: str, properties: Dict[str, Any]) -> None:
    """
    Add an entity to the knowledge graph.
    
    Args:
        graph (nx.MultiDiGraph): The knowledge graph
        entity_id (str): Unique identifier for the entity
        entity_type (str): Type of the entity as defined in the schema
        properties (Dict[str, Any]): Properties of the entity
        
    Returns:
        None
    """
    # Add node with entity type and properties
    graph.add_node(entity_id, entity_type=entity_type, **properties)
    logger.debug(f"Added entity {entity_id} of type {entity_type} to the graph")

def add_relation(
    graph: nx.MultiDiGraph, 
    source_id: str, 
    target_id: str, 
    relation_type: str, 
    properties: Dict[str, Any]
) -> None:
    """
    Add a relation between entities in the knowledge graph.
    
    Args:
        graph (nx.MultiDiGraph): The knowledge graph
        source_id (str): ID of the source entity
        target_id (str): ID of the target entity
        relation_type (str): Type of the relation as defined in the schema
        properties (Dict[str, Any]): Properties of the relation
        
    Returns:
        None
    """
    # Check if source and target entities exist
    if source_id not in graph:
        raise ValueError(f"Source entity {source_id} does not exist in the graph")
    if target_id not in graph:
        raise ValueError(f"Target entity {target_id} does not exist in the graph")
    
    # Add edge with relation type and properties
    graph.add_edge(source_id, target_id, relation_type=relation_type, **properties)
    logger.debug(f"Added relation {relation_type} from {source_id} to {target_id}")

def get_entity(graph: nx.MultiDiGraph, entity_id: str) -> Dict[str, Any]:
    """
    Get an entity from the knowledge graph.
    
    Args:
        graph (nx.MultiDiGraph): The knowledge graph
        entity_id (str): ID of the entity to retrieve
        
    Returns:
        Dict[str, Any]: Entity data including type and properties
        
    Raises:
        ValueError: If entity does not exist
    """
    if entity_id not in graph:
        raise ValueError(f"Entity {entity_id} does not exist in the graph")
    
    return graph.nodes[entity_id]

def get_relations(
    graph: nx.MultiDiGraph, 
    source_id: Optional[str] = None, 
    target_id: Optional[str] = None, 
    relation_type: Optional[str] = None
) -> List[Tuple[str, str, Dict[str, Any]]]:
    """
    Get relations from the knowledge graph, optionally filtered by source, target, or type.
    
    Args:
        graph (nx.MultiDiGraph): The knowledge graph
        source_id (Optional[str]): ID of the source entity to filter by
        target_id (Optional[str]): ID of the target entity to filter by
        relation_type (Optional[str]): Type of relation to filter by
        
    Returns:
        List[Tuple[str, str, Dict[str, Any]]]: List of tuples containing source ID, target ID, and relation data
    """
    result = []
    
    # Define which edges to iterate over based on provided filters
    if source_id is not None and target_id is not None:
        # Get edges between specific source and target
        if source_id in graph and target_id in graph and graph.has_edge(source_id, target_id):
            edges = [(source_id, target_id, edata) for _, _, edata in graph.edges(data=True) 
                     if graph.has_edge(source_id, target_id)]
        else:
            edges = []
    elif source_id is not None:
        # Get edges from specific source
        if source_id in graph:
            edges = [(source_id, t, edata) for _, t, edata in graph.out_edges(source_id, data=True)]
        else:
            edges = []
    elif target_id is not None:
        # Get edges to specific target
        if target_id in graph:
            edges = [(s, target_id, edata) for s, _, edata in graph.in_edges(target_id, data=True)]
        else:
            edges = []
    else:
        # Get all edges
        edges = [(s, t, edata) for s, t, edata in graph.edges(data=True)]
    
    # Filter by relation type if specified
    if relation_type is not None:
        result = [(s, t, edata) for s, t, edata in edges 
                 if 'relation_type' in edata and edata['relation_type'] == relation_type]
    else:
        result = edges
    
    return result

def get_entities_by_type(graph: nx.MultiDiGraph, entity_type: str) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Get all entities of a specific type from the knowledge graph.
    
    Args:
        graph (nx.MultiDiGraph): The knowledge graph
        entity_type (str): Type of entities to retrieve
        
    Returns:
        List[Tuple[str, Dict[str, Any]]]: List of tuples containing entity ID and entity data
    """
    return [(node_id, data) for node_id, data in graph.nodes(data=True) 
            if 'entity_type' in data and data['entity_type'] == entity_type]

def serialize_graph(graph: nx.MultiDiGraph, format: str = 'graphml') -> str:
    """
    Serialize the knowledge graph to a string in the specified format.
    
    Args:
        graph (nx.MultiDiGraph): The knowledge graph
        format (str): Format to serialize to ('graphml', 'gexf', 'json')
        
    Returns:
        str: Serialized graph
        
    Raises:
        ValueError: If format is not supported
    """
    import io
    from networkx.readwrite import json_graph
    
    if format == 'json':
        # For JSON format, use node_link_data directly
        data = json_graph.node_link_data(graph, edges="links")
        import json
        return json.dumps(data)
    
    # For other formats, use BytesIO and decode to string
    output = io.BytesIO()
    
    if format == 'graphml':
        nx.write_graphml(graph, output)
    elif format == 'gexf':
        nx.write_gexf(graph, output)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    # Convert bytes to string
    return output.getvalue().decode('utf-8')

def deserialize_graph(data: str, format: str = 'graphml') -> nx.MultiDiGraph:
    """
    Deserialize a string representation of a graph into a NetworkX graph.
    
    Args:
        data (str): Serialized graph data
        format (str): Format of the serialized data ('graphml', 'gexf', 'json')
        
    Returns:
        nx.MultiDiGraph: Deserialized knowledge graph
        
    Raises:
        ValueError: If format is not supported
    """
    import io
    from networkx.readwrite import json_graph
    
    if format == 'json':
        # For JSON format, parse the JSON string directly
        import json
        json_data = json.loads(data)
        return json_graph.node_link_graph(json_data, edges="links")
    
    # For other formats, convert string to bytes
    input_data = io.BytesIO(data.encode('utf-8'))
    
    if format == 'graphml':
        return nx.read_graphml(input_data)
    elif format == 'gexf':
        return nx.read_gexf(input_data)
    else:
        raise ValueError(f"Unsupported format: {format}")


def save_graph(graph: nx.MultiDiGraph, filepath: str, format: str = 'graphml') -> None:
    """
    Save the knowledge graph to a file.
    
    Args:
        graph (nx.MultiDiGraph): The knowledge graph
        filepath (str): Path to save the file to
        format (str): Format to save in ('graphml', 'gexf', 'json')
        
    Returns:
        None
        
    Raises:
        ValueError: If format is not supported
    """
    if format == 'graphml':
        nx.write_graphml(graph, filepath)
    elif format == 'gexf':
        nx.write_gexf(graph, filepath)
    elif format == 'json':
        from networkx.readwrite import json_graph
        import json
        data = json_graph.node_link_data(graph)
        with open(filepath, 'w') as f:
            json.dump(data, f)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    logger.info(f"Saved graph to {filepath} in {format} format")

def load_graph(filepath: str, format: str = 'graphml') -> nx.MultiDiGraph:
    """
    Load a knowledge graph from a file.
    
    Args:
        filepath (str): Path to the file
        format (str): Format of the file ('graphml', 'gexf', 'json')
        
    Returns:
        nx.MultiDiGraph: Loaded knowledge graph
        
    Raises:
        ValueError: If format is not supported
    """
    if format == 'graphml':
        return nx.read_graphml(filepath)
    elif format == 'gexf':
        return nx.read_gexf(filepath)
    elif format == 'json':
        from networkx.readwrite import json_graph
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
        return json_graph.node_link_graph(data)
    else:
        raise ValueError(f"Unsupported format: {format}")

def get_library_info() -> Dict[str, Any]:
    """
    Get information about the selected knowledge graph library.
    
    Returns:
        Dict[str, Any]: Information about the selected library
    """
    return KG_LIBRARY
