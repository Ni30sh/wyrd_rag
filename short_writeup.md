## Local RAG System for Wyrd Media Labs Wiki

### Overview

The goal of this project was to build a Retrieval-Augmented Generation (RAG) system that can answer questions about the Wyrd Media Labs company wiki. The system runs fully locally to avoid per-query API costs. It retrieves relevant information from the wiki documents and uses a local language model to generate answers.

The system pipeline is:

Documents → Chunking → Embeddings → Vector Database → Retrieval → Local LLM → Answer

### Document Processing

The company wiki was exported from Notion as multiple Markdown files. These files were loaded using a directory reader so that each page of the wiki could be processed as a document. Using Markdown files preserves the structure of the original wiki better than converting everything into a single document.

### Chunking Strategy

The documents were split using a sentence-based chunking strategy with:

* chunk_size = 700 characters
* chunk_overlap = 150 characters

The goal of chunking is to balance two competing requirements:

1. **Preserve enough context** so that the retrieved chunk contains meaningful information.
2. **Avoid overly large chunks** that reduce retrieval precision.

A chunk size of 700 characters was chosen because it typically captures a paragraph or a short section of the wiki, which is usually enough context for answering factual questions. The 150-character overlap helps ensure that important information near chunk boundaries is not lost between adjacent chunks.

Without overlap, answers that span across two chunks could be partially lost during retrieval.

### Embeddings

For semantic search, the system uses the `nomic-embed-text` model running locally through Ollama. This model converts text chunks into vector representations that capture semantic meaning. When a user asks a question, the question is embedded and compared against the stored document embeddings to retrieve the most relevant chunks.

Using a local embedding model ensures that the system has no external API dependency and avoids per-query costs.

### Vector Database

ChromaDB was used as the vector store because it is lightweight, easy to set up, and integrates directly with Python. It stores the embeddings for each document chunk and allows efficient similarity search to retrieve the most relevant pieces of text for a given query.

### Retrieval and Answer Generation

When a user asks a question, the system performs the following steps:

1. Convert the question into an embedding.
2. Retrieve the most similar document chunks from ChromaDB.
3. Pass those retrieved chunks as context to the local LLM (llama3 running through Ollama).
4. The LLM generates a final answer grounded in the retrieved context.

This approach ensures that the LLM does not rely solely on its internal knowledge and instead uses the company’s documentation as the primary source of truth.

### What I Would Improve

Several improvements could be made to make the system more robust:

* **Better chunking based on headings**: Instead of fixed-size chunks, the system could split documents based on Markdown headings or sections to preserve semantic structure.
* **Re-ranking retrieved chunks**: A cross-encoder model could be used to re-rank the retrieved results and improve answer accuracy.
* **Caching embeddings**: Persisting the vector database to disk would avoid recomputing embeddings each time the system runs.
* **Evaluation metrics**: Implementing retrieval metrics such as Recall@k would help evaluate whether the correct document sections are being retrieved.

### Where the System Breaks

There are several limitations in the current implementation:

* **Multi-hop questions**: If a question requires information from multiple distant sections of the wiki, the system may retrieve only one relevant chunk and miss the full context.
* **Ambiguous queries**: If the user asks a vague question, the retrieval step may return irrelevant chunks.
* **Terminology mismatch**: If a user uses terminology different from what appears in the wiki, the embedding model may fail to retrieve the correct document section.
* **Markdown formatting artifacts**: Since the source documents are Markdown exports from Notion, some formatting elements may introduce noise in the text.

### Conclusion

This implementation demonstrates a fully local RAG pipeline that retrieves information from internal documentation and generates answers without relying on external APIs. While the system works well for factual questions directly covered in the wiki, improvements in chunking strategy, retrieval ranking, and evaluation would further improve reliability.
