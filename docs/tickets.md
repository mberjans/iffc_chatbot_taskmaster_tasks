Okay, here is a detailed and exhaustive list of tickets for the "Nexus Scholar AI" development plan, designed for multiple coding agents working concurrently.

**Foundational Setup (Agent: DATA\_PREP)**

* **Ticket ID:** NXS-0Z-001  
  * **Title:** Create PubMed XML Downloader/Fetcher  
  * **Description:** Develop a Python script or function to download or fetch a single, full-text research paper in XML format from the PubMed Central Open Access subset. This script will provide the initial example XML file to be used by various modules during development. The script should save the XML file to a specified local path.  
  * **Inputs:** (Optional) Specific PubMed ID or search query.  
  * **Outputs:** Path to the downloaded XML file.  
  * **Agent:** DATA\_PREP  
  * **Dependencies:** None  
  * **Notes:** Consider using libraries like requests or BioPython if helpful, or pubmedparser2's download functionality.1  
* **Ticket ID:** NXS-1Z-001  
  * **Title:** Develop Core PubMed XML Parser Utility  
  * **Description:** Create a robust Python class or module (PubMedXMLParser) to parse the PubMed XML files. This utility will be used by multiple answering modules (KAG, GraphRAG, LightRAG, TraditionalRAG).  
  * **Inputs:** Path to a PubMed XML file.  
  * **Outputs:** A structured representation of the XML content (e.g., a dictionary or custom data objects). This should include:  
    * Clean full text.  
    * Distinct sections (e.g., abstract, introduction, methods, results, discussion, conclusion, references).  
    * Key metadata (e.g., PMID, title, authors, journal, publication date, keywords).  
  * **Agent:** DATA\_PREP  
  * **Dependencies:** NXS-0Z-001 (to have an example XML for testing).  
  * **Implementation Notes:** Strongly consider using the pubmedparser2 library, defining a comprehensive extraction structure.1 Ensure the output is easily consumable by other modules.

---

Phase 1: Develop Independent Answering Modules  
(The following agents can work concurrently after NXS-1Z-001 is complete for document-based modules)  
**Agent: KAG\_DEV (Knowledge Augmented Generation Module)**

* **Ticket ID:** NXS-1A-001  
  * **Title:** Implement KAG-Builder: XML to Knowledge Graph  
  * **Description:** Develop the KAG-Builder component of the KAG module. This involves processing parsed XML data to construct a knowledge graph (KG).  
  * **Inputs:** Structured data from NXS-1Z-001 (PubMedXMLParser).  
  * **Tasks:**  
    1. Define a schema for the biomedical KG (entities like medical terms, genes, proteins, methods, diseases; and their relationships).  
    2. Implement entity extraction (e.g., using spaCy with biomedical models, or LLM-based NER).  
    3. Implement relation extraction between identified entities.  
    4. Construct the KG (e.g., using NetworkX for in-memory representation or a simple on-disk format).  
    5. Implement mutual indexing: link KG nodes/edges back to specific text chunks/sections in the original XML for citation purposes.  
  * **Outputs:** A knowledge graph object or file, and the mutual indexing data structure.  
  * **Agent:** KAG\_DEV  
  * **Dependencies:** NXS-1Z-001.  
  * **Research:**.2  
* **Ticket ID:** NXS-1A-002  
  * **Title:** Implement KAG-Solver/Model: KG Querying and Answer Synthesis  
  * **Description:** Develop the KAG-Solver/Model component. This involves querying the KG and using an LLM to synthesize answers.  
  * **Inputs:**  
    1. User question (string).  
    2. Knowledge Graph and mutual indexing data from NXS-1A-001.  
    3. Path to the source XML file (for citation context).  
  * **Tasks:**  
    1. Develop methods to query the KG based on the user's question (e.g., identify entry nodes, graph traversal).  
    2. Retrieve relevant subgraphs or contextual information from the KG.  
    3. Pass the retrieved structured context to an LLM.  
    4. Prompt the LLM to synthesize a coherent natural language answer.  
    5. Generate accurate source citations using the mutual indexing data and the original XML.  
  * **Outputs:** A Python class/module that takes (XML file path, user question) and returns (answer string, list of citation strings/objects).  
  * **Agent:** KAG\_DEV  
  * **Dependencies:** NXS-1A-001.

**Agent: GRAPHRAG\_DEV (GraphRAG Module)**

* **Ticket ID:** NXS-1B-001  
  * **Title:** Implement GraphRAG Indexing Phase: XML to Document Knowledge Graph  
  * **Description:** Develop the indexing phase for the GraphRAG module. This involves constructing a graph from the input XML document.  
  * **Inputs:** Structured data from NXS-1Z-001 (PubMedXMLParser).  
  * **Tasks:**  
    1. Convert extracted text into a knowledge graph. Nodes can be text chunks (paragraphs/sentences) or extracted entities.  
    2. Establish edges based on criteria like sequential proximity, semantic similarity (requires embedding text chunks), explicit links in XML, or entity co-occurrence.  
    3. (Optional, advanced) Implement community detection within the graph and generate summaries for these communities.  
  * **Outputs:** An in-memory or on-disk graph representation.  
  * **Agent:** GRAPHRAG\_DEV  
  * **Dependencies:** NXS-1Z-001.  
  * **Research:**.4 Consider Microsoft's GraphRAG library/approach.4  
* **Ticket ID:** NXS-1B-002  
  * **Title:** Implement GraphRAG Querying Phase: Graph Traversal and Answer Synthesis  
  * **Description:** Develop the querying phase for the GraphRAG module.  
  * **Inputs:**  
    1. User question (string).  
    2. Graph representation from NXS-1B-001.  
    3. Path to the source XML file (for citation context).  
  * **Tasks:**  
    1. Implement local search (entity-focused graph traversal).  
    2. Implement global search (thematic queries, possibly using community summaries).  
    3. Retrieve relevant subgraphs, paths, or nodes as context.  
    4. Pass the retrieved graph-based context to an LLM.  
    5. Prompt the LLM to synthesize an answer.  
    6. Generate citations based on the source of the graph nodes/text chunks.  
  * **Outputs:** A Python class/module that takes (XML file path, user question) and returns (answer string, list of citation strings/objects).  
  * **Agent:** GRAPHRAG\_DEV  
  * **Dependencies:** NXS-1B-001.

**Agent: LIGHTRAG\_DEV (LightRAG Module)**

* **Ticket ID:** NXS-1C-001  
  * **Title:** Implement LightRAG Knowledge Graph and Vector Index Construction  
  * **Description:** Develop the data processing and indexing components for the LightRAG module.  
  * **Inputs:** Structured data from NXS-1Z-001 (PubMedXMLParser).  
  * **Tasks:**  
    1. Perform text chunking.  
    2. Implement entity and relationship extraction from text chunks.  
    3. Construct a knowledge graph from these entities and relationships.  
    4. Embed descriptions of entities and relationships into vectors.  
    5. Store these embeddings in a vector database (e.g., FAISS, ChromaDB, or nano\_vectordb as mentioned in LightRAG resources 10).  
  * **Outputs:** A knowledge graph and a vector index of entity/relationship embeddings.  
  * **Agent:** LIGHTRAG\_DEV  
  * **Dependencies:** NXS-1Z-001.  
  * **Research:**.7 Follow implementation patterns from LightRAG library/papers.  
* **Ticket ID:** NXS-1C-002  
  * **Title:** Implement LightRAG Dual-Level Retrieval and Answer Synthesis  
  * **Description:** Develop the query processing and answer generation components for the LightRAG module.  
  * **Inputs:**  
    1. User question (string).  
    2. Knowledge graph and vector index from NXS-1C-001.  
    3. Path to the source XML file (for citation context).  
  * **Tasks:**  
    1. Use an LLM to generate relevant keywords from the user question.  
    2. Implement low-level retrieval (specific entities/attributes from KG/vector index).  
    3. Implement high-level retrieval (broader concepts spanning multiple entities from KG/vector index).  
    4. Retrieve relevant entities and relationships (not just raw text chunks).  
    5. Pass the retrieved context to an LLM for answer synthesis.  
    6. Generate citations.  
  * **Outputs:** A Python class/module that takes (XML file path, user question) and returns (answer string, list of citation strings/objects).  
  * **Agent:** LIGHTRAG\_DEV  
  * **Dependencies:** NXS-1C-001.

**Agent: TRADRAG\_DEV (Traditional RAG Module)**

* **Ticket ID:** NXS-1D-001  
  * **Title:** Implement Traditional RAG: Text Processing and Vector Indexing  
  * **Description:** Develop the text processing and indexing pipeline for the Traditional RAG module.  
  * **Inputs:** Structured data from NXS-1Z-001 (PubMedXMLParser).  
  * **Tasks:**  
    1. Extract clean text content.  
    2. Implement text chunking strategies (e.g., by paragraph, fixed size with overlap).  
    3. Use a sentence-transformer model (e.g., all-MiniLM-L6-v2) to generate embeddings for each chunk.  
    4. Build a vector index (e.g., using FAISS or ChromaDB) to store chunks and their embeddings.  
  * **Outputs:** A vector index.  
  * **Agent:** TRADRAG\_DEV  
  * **Dependencies:** NXS-1Z-001.  
  * **Research:**.12  
* **Ticket ID:** NXS-1D-002  
  * **Title:** Implement Traditional RAG: Query Processing and Answer Synthesis  
  * **Description:** Develop the query processing and answer generation for the Traditional RAG module.  
  * **Inputs:**  
    1. User question (string).  
    2. Vector index from NXS-1D-001.  
    3. Path to the source XML file (for citation context, mapping chunks back to original doc).  
  * **Tasks:**  
    1. Embed the user question using the same sentence-transformer model.  
    2. Perform similarity search (k-NN) against the vector index to retrieve top-k relevant text chunks.  
    3. Pass retrieved chunks as context to an LLM.  
    4. Prompt LLM to synthesize an answer.  
    5. Generate citations from the source of the retrieved chunks.  
  * **Outputs:** A Python class/module that takes (XML file path, user question) and returns (answer string, list of citation strings/objects).  
  * **Agent:** TRADRAG\_DEV  
  * **Dependencies:** NXS-1D-001.

**Agent: WEBSEARCH\_DEV (Web-Search Module \- Perplexity API)**

* **Ticket ID:** NXS-1E-001  
  * **Title:** Implement Perplexity API Integration Wrapper  
  * **Description:** Create a Python class to handle interactions with the Perplexity API.  
  * **Inputs:** Perplexity API key.  
  * **Tasks:**  
    1. Securely manage API key.  
    2. Implement base function to send requests to Perplexity API (e.g., https://api.perplexity.ai/chat/completions).  
    3. Handle authentication (Bearer Token).  
    4. Parse JSON responses and implement error handling.  
  * **Outputs:** A reusable API client class.  
  * **Agent:** WEBSEARCH\_DEV  
  * **Dependencies:** None.  
  * **Research:**.13 Consult official Perplexity API documentation.  
* **Ticket ID:** NXS-1E-002  
  * **Title:** Implement query\_sonar\_online Method  
  * **Description:** Implement a method within the Web-Search module to query Perplexity using the sonar-online model.  
  * **Inputs:** User question (string).  
  * **Tasks:**  
    1. Use the NXS-1E-001 client to make an API call.  
    2. Specify the sonar-online model (e.g., sonar-small-online or sonar-medium-online) in the request.  
    3. Extract the answer and any source links from the response.  
  * **Outputs:** A Python method that takes (user question) and returns (answer string, list of source URLs).  
  * **Agent:** WEBSEARCH\_DEV  
  * **Dependencies:** NXS-1E-001.  
* **Ticket ID:** NXS-1E-003  
  * **Title:** Implement query\_sonar\_research Method  
  * **Description:** Implement a method within the Web-Search module to query Perplexity using the sonar-research model (Deep Research).  
  * **Inputs:** User question (string).  
  * **Tasks:**  
    1. Use the NXS-1E-001 client to make an API call.  
    2. Specify the sonar-research model in the request.  
    3. Extract the answer and any source links from the response.  
  * **Outputs:** A Python method that takes (user question) and returns (answer string, list of source URLs).  
  * **Agent:** WEBSEARCH\_DEV  
  * **Dependencies:** NXS-1E-001.

---

**Phase 2: Build the Evaluation Framework (Agent: EVAL\_FRAMEWORK\_DEV)**

* **Ticket ID:** NXS-2F-001  
  * **Title:** Design and Implement Multi-Module Test Harness Script  
  * **Description:** Create a Python script that can systematically run a test question through every answering module developed in Phase 1\.  
  * **Inputs:** Test question (string), path to source XML file (for document-based modules).  
  * **Tasks:**  
    1. Define a common interface or adapter layer for invoking each Phase 1 answering module (KAG, GraphRAG, LightRAG, TraditionalRAG, WebSearch-Online, WebSearch-Research).  
    2. Implement logic to instantiate and call each module with the test question and XML path.  
    3. Collect all generated answers and any accompanying metadata (citations, retrieved context).  
    4. Implement robust error handling for individual module failures.  
  * **Outputs:** A script that collects a list of (module\_name, answer\_object) tuples.  
  * **Agent:** EVAL\_FRAMEWORK\_DEV  
  * **Dependencies:** Defined interfaces for all Phase 1 modules (NXS-1A-002, NXS-1B-002, NXS-1C-002, NXS-1D-002, NXS-1E-002, NXS-1E-003).  
* **Ticket ID:** NXS-2F-002  
  * **Title:** Implement LLM-as-Judge Scoring Mechanism  
  * **Description:** Develop the component that uses a high-quality LLM (e.g., Gemini 1.5 Pro) to score answers from the test harness.  
  * **Inputs:**  
    1. Original test question.  
    2. Generated answer from a module.  
    3. Source text/retrieved context used by the module (if applicable).  
  * **Tasks:**  
    1. Define clear evaluation criteria (e.g., Factual Accuracy, Relevance, Completeness, Citation Quality) and a 1-10 scoring scale for each.  
    2. Craft a detailed prompt for the judge LLM, instructing it on the criteria, scale, and desired output format (e.g., JSON with scores and justifications).  
    3. Implement API calls to the chosen judge LLM.  
    4. Parse the judge LLM's response to extract scores and justifications.  
  * **Outputs:** A function that takes (question, answer, context) and returns a dictionary of scores.  
  * **Agent:** EVAL\_FRAMEWORK\_DEV  
  * **Dependencies:** NXS-2F-001 (to provide answers for scoring).  
  * **Research:** LightRAG's LLM-based answer comparison 10 could be an inspiration.  
* **Ticket ID:** NXS-2F-003  
  * **Title:** Implement Comparative Performance Report Generation  
  * **Description:** Create functionality to aggregate scores from the LLM-as-Judge and generate a detailed markdown report.  
  * **Inputs:** A list of (module\_name, answer\_object, scores\_dict) tuples for a given question.  
  * **Tasks:**  
    1. Structure the report to include the original question.  
    2. For each module: display its answer, scores for each criterion, and qualitative feedback from the judge.  
    3. Include an aggregated summary table comparing all modules.  
    4. Automate the generation of this markdown report.  
  * **Outputs:** A script/function that generates a markdown file.  
  * **Agent:** EVAL\_FRAMEWORK\_DEV  
  * **Dependencies:** NXS-2F-002.

---

**Phase 3: Design the Central Orchestrator (Agent: ORCHESTRATOR\_DEV)**

* **Ticket ID:** NXS-3F-001  
  * **Title:** Design and Implement Orchestrator Class Core Structure  
  * **Description:** Create the main Orchestrator Python class.  
  * **Tasks:**  
    1. Define the class structure.  
    2. Implement initialization to load/configure available expert answering modules (from Phase 1).  
    3. Implement a primary method to receive a user query.  
  * **Outputs:** Orchestrator class with basic query intake.  
  * **Agent:** ORCHESTRATOR\_DEV  
  * **Dependencies:** Defined interfaces for Phase 1 modules.  
* **Ticket ID:** NXS-3F-002  
  * **Title:** Implement Concurrent Mode for Module Execution in Orchestrator  
  * **Description:** Add functionality to the Orchestrator to run expert modules simultaneously using asyncio.  
  * **Inputs:** User query.  
  * **Tasks:**  
    1. Modify Orchestrator to use asyncio to invoke all (or a selected subset of) expert modules concurrently.  
    2. Gather results (answers, citations) as they become available from each asynchronous task.  
    3. Handle potential errors from individual async module calls.  
  * **Outputs:** Orchestrator capable of concurrent module execution.  
  * **Agent:** ORCHESTRATOR\_DEV  
  * **Dependencies:** NXS-3F-001.  
* **Ticket ID:** NXS-3F-003  
  * **Title:** Implement Sequential (Waterfall) Mode for Module Execution in Orchestrator  
  * **Description:** Add functionality to the Orchestrator to run modules in a logical "waterfall" sequence.  
  * **Inputs:** User query.  
  * **Tasks:**  
    1. Define a default sequence (e.g., fast RAG \-\> GraphRAG \-\> slow Perplexity deep research).  
    2. Implement logic to execute modules in this sequence.  
    3. (Optional but recommended) Implement an "early exit" strategy: after a module runs, quickly assess its answer quality; if sufficient, return it without running subsequent modules.  
  * **Outputs:** Orchestrator capable of sequential module execution.  
  * **Agent:** ORCHESTRATOR\_DEV  
  * **Dependencies:** NXS-3F-001.  
* **Ticket ID:** NXS-3F-004  
  * **Title:** Implement Real-time Answer Scoring Logic in Orchestrator  
  * **Description:** Integrate a real-time answer scoring mechanism into the Orchestrator, using or adapting the logic from Phase 2\.  
  * **Inputs:** Answers collected from modules (in either concurrent or sequential mode).  
  * **Tasks:**  
    1. Adapt the Phase 2 LLM-as-Judge logic (NXS-2F-002) for real-time use. This might involve:  
       * Using a smaller, faster LLM for scoring.  
       * Developing heuristic models for quick quality prediction.  
       * Using a simplified set of criteria.  
    2. Score each collected answer.  
  * **Outputs:** Orchestrator that scores answers from modules.  
  * **Agent:** ORCHESTRATOR\_DEV  
  * **Dependencies:** NXS-3F-001, NXS-2F-002 (for evaluation logic principles).  
* **Ticket ID:** NXS-3F-005  
  * **Title:** Implement Answer Selection Strategy in Orchestrator  
  * **Description:** Add logic to the Orchestrator to choose the single best answer to present to the user based on real-time scores.  
  * **Inputs:** Scored answers from NXS-3F-004.  
  * **Tasks:**  
    1. Implement a selection strategy (e.g., highest average score, highest score on a primary criterion, weighted scoring, rule-based selection).  
  * **Outputs:** Orchestrator that selects a single best answer.  
  * **Agent:** ORCHESTRATOR\_DEV  
  * **Dependencies:** NXS-3F-004.  
* **Ticket ID:** NXS-3F-006  
  * **Title:** Implement Hybrid Answer Synthesis Logic in Orchestrator  
  * **Description:** Add functionality for a hybrid answer mode where the Orchestrator synthesizes a comprehensive answer from the top 2-3 scored responses.  
  * **Inputs:** Top 2-3 scored answers. Original user question.  
  * **Tasks:**  
    1. Use an LLM as a "synthesis agent."  
    2. Craft a prompt for the synthesis LLM to combine insights, ensure factual accuracy, avoid redundancy, and maintain coherence.  
    3. Handle citation merging/preservation if possible.  
  * **Outputs:** Orchestrator capable of synthesizing a hybrid answer.  
  * **Agent:** ORCHESTRATOR\_DEV  
  * **Dependencies:** NXS-3F-004.

---

**Phase 4: Implement Agentic Prompt Optimization (Agent: PROMPT\_OPTIMIZER\_DEV)**

* **Ticket ID:** NXS-4G-001  
  * **Title:** Design and Implement PromptOptimizer Class  
  * **Description:** Create the PromptOptimizer Python class.  
  * **Tasks:** Define the class structure and its main method for optimizing a raw user question.  
  * **Outputs:** PromptOptimizer class structure.  
  * **Agent:** PROMPT\_OPTIMIZER\_DEV  
  * **Dependencies:** None.  
* **Ticket ID:** NXS-4G-002  
  * **Title:** Implement Magnetic RAG Algorithm in PromptOptimizer  
  * **Description:** Implement the Magnetic RAG algorithm as described in the plan. This involves rewriting a raw user question into a more detailed, explicit prompt with placeholder slots for evidence.  
  * **Inputs:** Raw user question (string).  
  * **Tasks:**  
    1. Use an LLM to perform the query transformation.  
    2. Develop few-shot prompts or fine-tuning strategies for the LLM to achieve the desired "magnetic" prompt structure (detailed, explicit, with evidence placeholders).  
  * **Outputs:** A method within PromptOptimizer that returns the optimized prompt string.  
  * **Agent:** PROMPT\_OPTIMIZER\_DEV  
  * **Dependencies:** NXS-4G-001.  
  * **Research:** Focus on the plan's description of "Magnetic RAG." General query expansion/rewriting techniques 18 can provide foundational ideas.  
* **Ticket ID:** NXS-4G-003  
  * **Title:** Integrate PromptOptimizer into the Central Orchestrator  
  * **Description:** Modify the Orchestrator to use the PromptOptimizer before sending queries to expert modules.  
  * **Tasks:**  
    1. The Orchestrator (NXS-3F-001) should instantiate and call the PromptOptimizer (NXS-4G-002) with the raw user query.  
    2. The optimized prompt generated by PromptOptimizer should then be passed to the expert answering modules.  
    3. Consider if the optimized prompt needs tailoring for different module types (RAG, KG, Perplexity).  
  * **Agent:** PROMPT\_OPTIMIZER\_DEV (or could be ORCHESTRATOR\_DEV if integration is complex)  
  * **Dependencies:** NXS-3F-001 (Orchestrator), NXS-4G-002 (PromptOptimizer).

---

**Phase 5: Construct the Streamlit Web Interface (Agent: UI\_UX\_DEPLOY\_DEV)**

* **Ticket ID:** NXS-5H-001  
  * **Title:** Develop Main Streamlit App File and Basic Chat Interface  
  * **Description:** Create the main Streamlit application file (app.py or similar) and implement a basic chat interface.  
  * **Tasks:**  
    1. Use st.chat\_input() for user queries.  
    2. Use st.chat\_message() to display user messages and assistant responses.  
    3. Manage chat history using st.session\_state.  
  * **Outputs:** A functional Streamlit app with a basic chat UI.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** None.  
* **Ticket ID:** NXS-5H-002  
  * **Title:** Implement Backend Orchestrator Invocation from Streamlit  
  * **Description:** Connect the Streamlit frontend to the backend Orchestrator.  
  * **Inputs:** User query from st.chat\_input().  
  * **Tasks:**  
    1. When a user submits a query, call the main processing method of the Orchestrator (NXS-3F-001 and its subsequent enhancements like NXS-4G-003).  
    2. This will likely involve running the Orchestrator in a separate thread to avoid blocking the Streamlit UI.  
    3. Retrieve the final answer from the Orchestrator.  
  * **Outputs:** Streamlit app that sends queries to the backend and displays results.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-3F-001 (Orchestrator interface), NXS-4G-003 (Orchestrator with PromptOptimizer), NXS-5H-001.  
* **Ticket ID:** NXS-5H-003  
  * **Title:** Implement Real-time Progress Status Indicator in Streamlit  
  * **Description:** Display real-time progress updates from the backend Orchestrator in the Streamlit UI.  
  * **Tasks:**  
    1. Modify the Orchestrator (NXS-3F-001 onwards) to push status updates (e.g., "Querying GraphRAG...", "Evaluating answers...") to a shared thread-safe queue or state object.  
    2. In the Streamlit frontend, use st.empty() or st.status() 22 to create a placeholder for progress messages.  
    3. Implement a polling mechanism in Streamlit (e.g., a loop with time.sleep()) to check the shared queue/state and update the placeholder.  
  * **Outputs:** Streamlit UI showing live progress updates.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-5H-002. Orchestrator needs modification.  
  * **Research:**.22  
* **Ticket ID:** NXS-5H-004  
  * **Title:** Implement Response Streaming using st.write\_stream in Streamlit  
  * **Description:** Display the final answer from the Orchestrator token-by-token.  
  * **Tasks:**  
    1. Modify the Orchestrator's final answer generation step (especially if it involves an LLM call for synthesis or from a streaming-capable module) to be a generator function that yields tokens or small text chunks.  
    2. In the Streamlit frontend, use st.write\_stream() to consume this generator and display the answer as it arrives.  
  * **Outputs:** Streamlit UI with streaming answer display.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-5H-002. Orchestrator needs modification.

---

**Phase 6: Finalize as a Production-Ready, Multi-User Website (Agent: UI\_UX\_DEPLOY\_DEV)**

* **Ticket ID:** NXS-6H-001  
  * **Title:** Design Database Schema for User Accounts and Chat History  
  * **Description:** Define the database schema for managing users, chat sessions, and messages.  
  * **Tasks:**  
    1. Define Users table (e.g., user\_id, username, email, hashed\_password, role).  
    2. Define ChatSessions table (e.g., session\_id, user\_id, session\_name, created\_at).  
    3. Define ChatMessages table (e.g., message\_id, session\_id, timestamp, role, content).  
    4. Consider schema for both SQLite (development) and PostgreSQL (production).  
  * **Outputs:** SQL schema definitions or ORM model definitions.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** None.  
* **Ticket ID:** NXS-6H-002  
  * **Title:** Implement Database Integration Layer (ORM)  
  * **Description:** Set up an Object-Relational Mapper (e.g., SQLAlchemy) to interact with the database.  
  * **Tasks:**  
    1. Install and configure SQLAlchemy (or chosen ORM).  
    2. Create ORM models corresponding to the schema in NXS-6H-001.  
    3. Implement basic CRUD (Create, Read, Update, Delete) utility functions for these models.  
  * **Outputs:** ORM models and database utility functions.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-6H-001.  
* **Ticket ID:** NXS-6H-003  
  * **Title:** Implement User Account Management Backend Logic  
  * **Description:** Develop backend logic for user registration (if not solely relying on OIDC for user creation), login (if custom), and role management.  
  * **Tasks:**  
    1. (If applicable) User registration endpoint/logic.  
    2. (If applicable) Password hashing and secure storage.  
    3. Functions to retrieve user details and roles.  
  * **Outputs:** Backend functions for user account management.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-6H-002.  
* **Ticket ID:** NXS-6H-004  
  * **Title:** Implement Chat History Storage and Retrieval Backend Logic  
  * **Description:** Develop backend logic to save chat messages to the database and retrieve chat history for users.  
  * **Tasks:**  
    1. Function to save new chat messages (user and assistant) to ChatMessages and link to ChatSessions.  
    2. Function to retrieve all messages for a given session\_id.  
    3. Function to retrieve all chat sessions for a given user\_id.  
  * **Outputs:** Backend functions for chat history management.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-6H-002.  
* **Ticket ID:** NXS-6H-005  
  * **Title:** Implement Streamlit User Authentication (OIDC)  
  * **Description:** Integrate OpenID Connect for user authentication in the Streamlit app.  
  * **Tasks:**  
    1. Set up an OIDC provider (e.g., Google Identity, Auth0).  
    2. Configure secrets.toml with OIDC client credentials (client\_id, client\_secret, server\_metadata\_url, redirect\_uri, cookie\_secret).  
    3. Use st.login(), st.user, and st.logout() in the Streamlit app to manage login flows.  
    4. Ensure user information (e.g., email) from st.user can be used to link to the backend Users table.  
  * **Outputs:** Streamlit app with working user authentication.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-5H-001.  
  * **Research:**.24  
* **Ticket ID:** NXS-6H-006  
  * **Title:** Create Admin-Only Pages in Streamlit  
  * **Description:** Develop admin-specific pages within the Streamlit application.  
  * **Tasks:**  
    1. Use Streamlit's multipage app feature (files in pages/ directory).  
    2. Implement role-based access control: check st.user information (potentially linked to Users table role via NXS-6H-003) to show/hide admin pages/elements.  
    3. Design basic layout for admin functionalities (user management, document upload).  
  * **Outputs:** Admin section in the Streamlit app.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-6H-005.  
* **Ticket ID:** NXS-6H-007  
  * **Title:** Implement Admin Upload Feature UI (XML & PDF)  
  * **Description:** Create the UI for administrators to upload new research papers.  
  * **Tasks:**  
    1. On an admin page (NXS-6H-006), use st.file\_uploader to allow selection of XML and PDF files.  
    2. Handle file submission to a backend endpoint/process.  
  * **Outputs:** File upload interface for admins.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-6H-006.  
* **Ticket ID:** NXS-6H-008  
  * **Title:** Implement Chat History Display UI for Users  
  * **Description:** Create the UI for authenticated users to view and continue their past conversations.  
  * **Tasks:**  
    1. After login (NXS-6H-005), fetch the user's past chat sessions using backend logic from NXS-6H-004.  
    2. Display a list of past sessions (e.g., by name or date).  
    3. Allow users to select a session to load its messages into the main chat interface (NXS-5H-001).  
  * **Outputs:** Chat history viewing functionality in the UI.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-5H-001, NXS-6H-004, NXS-6H-005.  
* **Ticket ID:** NXS-6I-001  
  * **Title:** Implement PDF Parsing Module  
  * **Description:** Create a module to extract text content from PDF files.  
  * **Tasks:**  
    1. Use a library like PyMuPDF (fitz) to open PDF files and extract raw text.  
    2. Handle potential errors during PDF parsing.  
  * **Outputs:** A function that takes a PDF file path and returns extracted text.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV (or a dedicated backend agent if workload is split)  
  * **Dependencies:** None.  
  * **Research:**.26  
* **Ticket ID:** NXS-6I-002  
  * **Title:** Implement Asynchronous Backend Task for Knowledge Store Updates  
  * **Description:** Develop the backend process triggered by admin file uploads (NXS-6H-007) to parse new documents and update all relevant RAG and KG knowledge stores.  
  * **Tasks:**  
    1. Set up an asynchronous task queue (e.g., Celery with RabbitMQ/Redis, or concurrent.futures for simpler setups).  
    2. When a file is uploaded, this task should:  
       * Use NXS-1Z-001 (XML Parser) or NXS-6I-001 (PDF Parser) to process the document.  
       * Call the appropriate update/indexing methods for each document-based answering module (KAG, GraphRAG, LightRAG, TraditionalRAG) to incorporate the new document into their respective knowledge stores.  
    3. Provide a mechanism for the admin UI to get status updates on the ingestion process (e.g., "pending," "processing," "completed," "failed").  
  * **Outputs:** A robust, asynchronous document ingestion pipeline.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV (or a dedicated backend agent)  
  * **Dependencies:** NXS-1Z-001, NXS-6I-001, NXS-6H-007, and interfaces for updating Phase 1 module knowledge stores.  
* **Ticket ID:** NXS-6J-001  
  * **Title:** Prepare Streamlit Application for Production Deployment  
  * **Description:** Configure the Streamlit application with settings suitable for a production environment.  
  * **Tasks:**  
    1. Create/update config.toml with production settings (e.g., server.headless \= true, appropriate logging levels, server.maxUploadSize).  
    2. Ensure all Python dependencies are pinned in requirements.txt.  
  * **Outputs:** Production-ready Streamlit configuration.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-5H-001.  
* **Ticket ID:** NXS-6J-002  
  * **Title:** Create Sample NGINX Configuration for Reverse Proxy  
  * **Description:** Provide a sample nginx.conf file to demonstrate how to set up NGINX as a reverse proxy in front of the Streamlit application.  
  * **Tasks:**  
    1. Configure NGINX to proxy requests to the Streamlit app.  
    2. Include SSL termination (HTTPS).  
    3. Ensure correct proxying of WebSocket connections (essential for Streamlit interactivity using proxy\_set\_header Upgrade $http\_upgrade; and proxy\_set\_header Connection "upgrade";).  
    4. Set appropriate timeouts and headers.  
  * **Outputs:** A sample nginx.conf file and deployment instructions.  
  * **Agent:** UI\_UX\_DEPLOY\_DEV  
  * **Dependencies:** NXS-6J-001.  
  * **Research:**.28