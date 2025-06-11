"""Unit tests for the NER Tool module.

This module contains tests for the Named Entity Recognition (NER) Tool
functionality in the KAG module.
"""

import unittest
import os
import sys
import json
import tempfile

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.kag.ner import (
    NERTool, 
    DummyNERBackend,
    Entity,
    BIOMEDICAL_ENTITY_TYPES,
    NER_BACKENDS
)

class TestEntity(unittest.TestCase):
    """Test cases for the Entity class."""
    
    def test_entity_initialization(self):
        """Test Entity initialization and properties."""
        text = "BRCA1"
        entity_type = "GENE"
        start_char = 10
        end_char = 15
        source_text = "The BRCA1 gene is associated with breast cancer."
        
        entity = Entity(text, entity_type, start_char, end_char, source_text)
        
        self.assertEqual(entity.text, text)
        self.assertEqual(entity.entity_type, entity_type)
        self.assertEqual(entity.start_char, start_char)
        self.assertEqual(entity.end_char, end_char)
        self.assertEqual(entity.source_text, source_text)
    
    def test_entity_context(self):
        """Test getting context around an entity."""
        source_text = "The BRCA1 gene is associated with breast cancer and ovarian cancer."
        entity = Entity("BRCA1", "GENE", 4, 9, source_text)
        
        # Test with default window
        context = entity.get_context()
        self.assertIn("The BRCA1 gene is associated with", context)
        
        # Test with custom window
        context = entity.get_context(10)
        self.assertIn("The BRCA1 gene", context)
        self.assertTrue(len(context) <= 30)  # 10 chars before + entity (5 chars) + 10 chars after + some potential margin
    
    def test_entity_to_dict(self):
        """Test converting an entity to a dictionary."""
        entity = Entity("BRCA1", "GENE", 4, 9, "Sample text")
        
        entity_dict = entity.to_dict()
        
        self.assertEqual(entity_dict["text"], "BRCA1")
        self.assertEqual(entity_dict["entity_type"], "GENE")
        self.assertEqual(entity_dict["start_char"], 4)
        self.assertEqual(entity_dict["end_char"], 9)
        self.assertIn("description", entity_dict)


class TestDummyNERBackend(unittest.TestCase):
    """Test cases for the DummyNERBackend."""
    
    def test_extract_entities_gene(self):
        """Test extracting gene entities."""
        backend = DummyNERBackend()
        text = "BRCA1 is a human tumor suppressor gene."
        
        entities = backend.extract_entities(text)
        
        # Find gene entities (BRCA1)
        gene_entities = []
        for entity in entities:
            if entity.entity_type == "GENE":
                gene_entities.append(entity)
        
        self.assertTrue(len(gene_entities) > 0)
        
        found_brca1 = False
        for entity in gene_entities:
            if entity.text == "BRCA1":
                found_brca1 = True
                break
        
        self.assertTrue(found_brca1, "Should detect BRCA1 as a gene")
    
    def test_extract_entities_disease(self):
        """Test extracting disease entities."""
        backend = DummyNERBackend()
        text = "Cancer is a group of diseases involving abnormal cell growth."
        
        entities = backend.extract_entities(text)
        
        # Find disease entities (cancer)
        disease_entities = []
        for entity in entities:
            if entity.entity_type == "DISEASE":
                disease_entities.append(entity)
        
        self.assertTrue(len(disease_entities) > 0)
        
        found_cancer = False
        for entity in disease_entities:
            if entity.text.lower() == "cancer":
                found_cancer = True
                break
        
        self.assertTrue(found_cancer, "Should detect 'cancer' as a disease")
    
    def test_extract_entities_empty_text(self):
        """Test extracting entities from empty text."""
        backend = DummyNERBackend()
        
        entities = backend.extract_entities("")
        self.assertEqual(len(entities), 0)
        
        entities = backend.extract_entities(None)
        self.assertEqual(len(entities), 0)


class TestNERTool(unittest.TestCase):
    """Test cases for the NERTool."""
    
    def test_initialization_with_dummy_backend(self):
        """Test initializing the NER tool with the dummy backend."""
        ner_tool = NERTool(backend="dummy")
        
        self.assertEqual(ner_tool.backend_name, "dummy")
        self.assertIsInstance(ner_tool.backend, DummyNERBackend)
    
    def test_initialization_with_invalid_backend(self):
        """Test initializing the NER tool with an invalid backend."""
        with self.assertRaises(ValueError):
            NERTool(backend="invalid_backend")
    
    def test_extract_entities(self):
        """Test extracting entities from text."""
        ner_tool = NERTool(backend="dummy")
        
        text = "BRCA1 is associated with breast cancer."
        entities = ner_tool.extract_entities(text)
        
        self.assertTrue(len(entities) > 0)
    
    def test_extract_entities_empty_text(self):
        """Test extracting entities from empty text."""
        ner_tool = NERTool(backend="dummy")
        
        entities = ner_tool.extract_entities("")
        self.assertEqual(len(entities), 0)
        
        entities = ner_tool.extract_entities(None)
        self.assertEqual(len(entities), 0)
    
    def test_process_document(self):
        """Test processing a document to extract entities."""
        ner_tool = NERTool(backend="dummy")
        
        document = {
            "id": "doc1",
            "title": "BRCA1 and breast cancer",
            "abstract": "This paper discusses BRCA1's role in breast cancer.",
            "full_text": "BRCA1 is a tumor suppressor gene that plays a role in DNA repair and is associated with hereditary breast and ovarian cancer syndrome."
        }
        
        processed_doc = ner_tool.process_document(document)
        
        self.assertIn("title_entities", processed_doc)
        self.assertIn("abstract_entities", processed_doc)
        self.assertIn("full_text_entities", processed_doc)
        
        self.assertTrue(len(processed_doc["title_entities"]) > 0)
        self.assertTrue(len(processed_doc["abstract_entities"]) > 0)
        self.assertTrue(len(processed_doc["full_text_entities"]) > 0)
    
    def test_long_text_processing(self):
        """Test processing a document with long text."""
        ner_tool = NERTool(backend="dummy")
        
        # Create a long text with repeated mentions of genes and diseases
        long_text = "BRCA1 " * 1000 + "cancer " * 1000
        
        document = {
            "id": "doc2",
            "full_text": long_text
        }
        
        processed_doc = ner_tool.process_document(document)
        
        self.assertIn("full_text_entities", processed_doc)
        self.assertTrue(len(processed_doc["full_text_entities"]) > 0)
    
    def test_get_backend_info(self):
        """Test getting information about the backend."""
        ner_tool = NERTool(backend="dummy")
        
        backend_info = ner_tool.get_backend_info()
        
        self.assertEqual(backend_info["name"], "Dummy NER")
        self.assertFalse(backend_info["requires_install"])
    
    def test_list_available_backends(self):
        """Test listing available backends."""
        backends = NERTool.list_available_backends()
        
        self.assertIn("dummy", backends)
        self.assertIn("spacy", backends)
        self.assertIn("scispacy", backends)
    
    def test_check_backend_availability(self):
        """Test checking if a backend is available."""
        # The dummy backend should always be available
        is_available, _ = NERTool.check_backend_availability("dummy")
        self.assertTrue(is_available)
        
        # Test with an invalid backend
        with self.assertRaises(ValueError):
            NERTool.check_backend_availability("invalid_backend")

# Add main test execution
if __name__ == "__main__":
    unittest.main()

    def test_init(self):
        """Test initialization of NERTool."""
        # Test with default model
        ner_tool = NERTool()
        self.assertEqual(ner_tool.model_name, "en_core_sci_sm")
        self.assertFalse(ner_tool.is_loaded)
        
        # Test with specified model
        ner_tool = NERTool(model_name="en_core_sci_md")
        self.assertEqual(ner_tool.model_name, "en_core_sci_md")
        
        # Test with invalid model
        with self.assertRaises(ValueError):
            NERTool(model_name="invalid_model")
    
    @patch('spacy.load')
    def test_load_model(self, mock_load):
        """Test loading a model."""
        # Mock the spacy.load function
        mock_nlp = MagicMock()
        mock_load.return_value = mock_nlp
        
        ner_tool = NERTool()
        ner_tool.load_model()
        
        # Check that spacy.load was called with the correct model name
        mock_load.assert_called_once_with("en_core_sci_sm")
        self.assertTrue(ner_tool.is_loaded)
        self.assertEqual(ner_tool.nlp, mock_nlp)
    
    @patch('spacy.load')
    @patch('subprocess.check_call')
    def test_load_model_not_installed(self, mock_check_call, mock_load):
        """Test loading a model that is not installed."""
        # First call raises OSError (model not found), second call succeeds
        mock_load.side_effect = [OSError(), MagicMock()]
        
        ner_tool = NERTool()
        ner_tool.load_model()
        
        # Check that pip install was called with the correct URL
        mock_check_call.assert_called_once()
        self.assertIn("pip", mock_check_call.call_args[0][0])
        self.assertIn("install", mock_check_call.call_args[0][0])
        self.assertEqual(mock_check_call.call_args[0][0][2], NER_MODELS["en_core_sci_sm"]["url"])
        
        # Check that spacy.load was called twice (first fails, second succeeds)
        self.assertEqual(mock_load.call_count, 2)
        self.assertTrue(ner_tool.is_loaded)
    
    @patch('spacy.load')
    def test_extract_entities_empty_text(self, mock_load):
        """Test extracting entities from empty text."""
        # Mock the spacy.load function
        mock_nlp = MagicMock()
        mock_load.return_value = mock_nlp
        
        ner_tool = NERTool()
        ner_tool.load_model()
        
        # Test with empty text
        entities = ner_tool.extract_entities("")
        self.assertEqual(entities, [])
        
        # Test with whitespace-only text
        entities = ner_tool.extract_entities("   ")
        self.assertEqual(entities, [])
    
    @patch('spacy.load')
    def test_extract_entities(self, mock_load):
        """Test extracting entities from text."""
        # Create a mock Doc with entities
        mock_doc = MagicMock()
        mock_ent1 = MagicMock()
        mock_ent1.text = "BRCA1"
        mock_ent1.start_char = 10
        mock_ent1.end_char = 15
        mock_ent1.label_ = "GENE"
        
        mock_ent2 = MagicMock()
        mock_ent2.text = "breast cancer"
        mock_ent2.start_char = 30
        mock_ent2.end_char = 43
        mock_ent2.label_ = "DISEASE"
        
        mock_doc.ents = [mock_ent1, mock_ent2]
        
        # Mock the NLP pipeline
        mock_nlp = MagicMock()
        mock_nlp.return_value = mock_doc
        mock_load.return_value = mock_nlp
        
        # Create NERTool and extract entities
        ner_tool = NERTool()
        ner_tool.load_model()
        
        # Mock the _get_entity_context method
        ner_tool._get_entity_context = MagicMock()
        ner_tool._get_entity_context.return_value = "context"
        
        entities = ner_tool.extract_entities("Test text with BRCA1 gene and breast cancer disease")
        
        # Check that the correct entities were extracted
        self.assertEqual(len(entities), 2)
        
        self.assertEqual(entities[0]["text"], "BRCA1")
        self.assertEqual(entities[0]["start_char"], 10)
        self.assertEqual(entities[0]["end_char"], 15)
        self.assertEqual(entities[0]["label"], "GENE")
        self.assertEqual(entities[0]["description"], "Gene or gene product")
        self.assertEqual(entities[0]["context"], "context")
        
        self.assertEqual(entities[1]["text"], "breast cancer")
        self.assertEqual(entities[1]["start_char"], 30)
        self.assertEqual(entities[1]["end_char"], 43)
        self.assertEqual(entities[1]["label"], "DISEASE")
        self.assertEqual(entities[1]["description"], "Disease or syndrome")
        self.assertEqual(entities[1]["context"], "context")
    
    @patch('spacy.load')
    def test_process_document(self, mock_load):
        """Test processing a document."""
        # Create a mock Doc with entities
        mock_doc = MagicMock()
        mock_doc.ents = []
        
        # Mock the NLP pipeline
        mock_nlp = MagicMock()
        mock_nlp.return_value = mock_doc
        mock_load.return_value = mock_nlp
        
        # Create NERTool
        ner_tool = NERTool()
        ner_tool.load_model()
        
        # Mock the extract_entities method
        ner_tool.extract_entities = MagicMock()
        ner_tool.extract_entities.return_value = [{"text": "entity"}]
        
        # Test document with title and abstract
        document = {
            "id": "doc1",
            "title": "Test Title",
            "abstract": "Test Abstract"
        }
        
        processed_doc = ner_tool.process_document(document)
        
        # Check that extract_entities was called for title and abstract
        self.assertEqual(ner_tool.extract_entities.call_count, 2)
        self.assertEqual(processed_doc["title_entities"], [{"text": "entity"}])
        self.assertEqual(processed_doc["abstract_entities"], [{"text": "entity"}])
        
        # Test document with full text
        document = {
            "id": "doc2",
            "title": "Test Title",
            "abstract": "Test Abstract",
            "full_text": "Test Full Text"
        }
        
        ner_tool.extract_entities.reset_mock()
        processed_doc = ner_tool.process_document(document)
        
        # Check that extract_entities was called for title, abstract, and full text
        self.assertEqual(ner_tool.extract_entities.call_count, 3)
        self.assertEqual(processed_doc["title_entities"], [{"text": "entity"}])
        self.assertEqual(processed_doc["abstract_entities"], [{"text": "entity"}])
        self.assertEqual(processed_doc["full_text_entities"], [{"text": "entity"}])
    
    @patch('spacy.load')
    def test_process_document_long_text(self, mock_load):
        """Test processing a document with long text."""
        # Create a mock Doc with entities
        mock_doc = MagicMock()
        mock_doc.ents = []
        
        # Mock the NLP pipeline
        mock_nlp = MagicMock()
        mock_nlp.return_value = mock_doc
        mock_load.return_value = mock_nlp
        
        # Create NERTool
        ner_tool = NERTool()
        ner_tool.load_model()
        
        # Mock the extract_entities method
        ner_tool.extract_entities = MagicMock()
        ner_tool.extract_entities.return_value = [{"text": "entity", "start_char": 0, "end_char": 6}]
        
        # Mock the _split_text_into_chunks method
        ner_tool._split_text_into_chunks = MagicMock()
        ner_tool._split_text_into_chunks.return_value = [
            {"text": "chunk1", "offset": 0},
            {"text": "chunk2", "offset": 5000}
        ]
        
        # Test document with long full text
        document = {
            "id": "doc3",
            "title": "Test Title",
            "abstract": "Test Abstract",
            "full_text": "X" * 15000  # Long text
        }
        
        processed_doc = ner_tool.process_document(document)
        
        # Check that _split_text_into_chunks was called
        ner_tool._split_text_into_chunks.assert_called_once()
        
        # Check that extract_entities was called for each chunk
        self.assertEqual(ner_tool.extract_entities.call_count, 4)  # title, abstract, 2 chunks
    
    def test_get_model_info(self):
        """Test getting model information."""
        ner_tool = NERTool(model_name="en_core_sci_sm")
        info = ner_tool.get_model_info()
        
        self.assertEqual(info["description"], "Small English biomedical model")
        self.assertEqual(info["size"], "small")
        self.assertEqual(info["languages"], ["en"])
        self.assertEqual(info["license"], "MIT")
        self.assertEqual(info["author"], "Allen AI")
    
    def test_get_entity_description(self):
        """Test getting entity description."""
        ner_tool = NERTool()
        
        # Test with known entity type
        desc = ner_tool._get_entity_description("GENE")
        self.assertEqual(desc, "Gene or gene product")
        
        # Test with unknown entity type
        desc = ner_tool._get_entity_description("UNKNOWN")
        self.assertEqual(desc, "UNKNOWN")
    
    @patch('spacy.load')
    def test_get_entity_context(self, mock_load):
        """Test getting entity context."""
        # Create a mock Doc
        mock_doc = MagicMock()
        mock_doc.__getitem__.return_value.text = "context text"
        
        # Create a mock entity
        mock_entity = MagicMock()
        mock_entity.start = 10
        mock_entity.end = 15
        
        # Create NERTool
        ner_tool = NERTool()
        
        # Test getting context
        context = ner_tool._get_entity_context(mock_doc, mock_entity)
        self.assertEqual(context, "context text")
        
        # Check that the correct slice was requested
        mock_doc.__getitem__.assert_called_once()
        args = mock_doc.__getitem__.call_args[0][0]
        self.assertEqual(args.start, 5)  # start - window
        self.assertEqual(args.stop, 20)  # end + window
    
    def test_split_text_into_chunks(self):
        """Test splitting text into chunks."""
        ner_tool = NERTool()
        
        # Test with short text (no splitting needed)
        text = "Short text"
        chunks = ner_tool._split_text_into_chunks(text, chunk_size=100, overlap=10)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["text"], "Short text")
        self.assertEqual(chunks[0]["offset"], 0)
        
        # Test with text that needs splitting
        text = "This is a longer text that needs to be split into chunks. " * 10
        chunks = ner_tool._split_text_into_chunks(text, chunk_size=100, overlap=20)
        
        self.assertTrue(len(chunks) > 1)
        self.assertEqual(chunks[0]["offset"], 0)
        
        # Check that chunks have the correct offsets and overlaps
        for i in range(1, len(chunks)):
            prev_end = chunks[i-1]["offset"] + len(chunks[i-1]["text"])
            curr_start = chunks[i]["offset"]
            self.assertTrue(prev_end > curr_start)  # Should overlap
            self.assertTrue(prev_end - curr_start <= 20)  # Overlap should be at most 20
    
    def test_list_available_models(self):
        """Test listing available models."""
        models = NERTool.list_available_models()
        
        self.assertIsInstance(models, dict)
        self.assertIn("en_core_sci_sm", models)
        self.assertIn("en_core_sci_md", models)
        self.assertIn("en_ner_bc5cdr_md", models)
        self.assertIn("en_ner_bionlp13cg_md", models)
        
        # Check model details
        self.assertEqual(models["en_core_sci_sm"]["size"], "small")
        self.assertEqual(models["en_core_sci_md"]["size"], "medium")
    
    @patch('subprocess.check_call')
    def test_install_model(self, mock_check_call):
        """Test installing a model."""
        # Test with valid model
        result = NERTool.install_model("en_core_sci_sm")
        self.assertTrue(result)
        mock_check_call.assert_called_once()
        self.assertIn("pip", mock_check_call.call_args[0][0])
        self.assertIn("install", mock_check_call.call_args[0][0])
        
        # Test with invalid model
        with self.assertRaises(ValueError):
            NERTool.install_model("invalid_model")
        
        # Test with installation failure
        mock_check_call.reset_mock()
        mock_check_call.side_effect = Exception("Installation failed")
        result = NERTool.install_model("en_core_sci_md")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
