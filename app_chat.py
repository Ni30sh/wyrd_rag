"""
Gradio Chat Interface for RAG System
Interactive question-answering interface with Gradio
"""

import gradio as gr
from pathlib import Path
from typing import Optional
import sys

# LlamaIndex imports
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser

# Configuration
BASE_URL = "http://localhost:11434"
LLM_MODEL = "mistral"
EMBED_MODEL = "nomic-embed-text"
CHROMA_DIR = Path("data/vector_store/chroma_llamaindex")
COLLECTION_NAME = "support_inbox_llamaindex"

# Load data paths
DATA_DIR = Path("data")
DEFAULT_WIKI_DIR = DATA_DIR / "wiki_docs"

# Global variables
query_engine = None
chat_history = []


def load_wiki_markdown_docs(wiki_dir: Path):
    """Load markdown documents from wiki directory."""
    from llama_index.core import SimpleDirectoryReader
    documents = []
    try:
        reader = SimpleDirectoryReader(input_dir=str(wiki_dir), recursive=True,
                                       required_exts=[".md"])
        documents = reader.load_data()
        # Add metadata
        for doc in documents:
            doc.metadata["source"] = str(wiki_dir)
        print(f"✅ Loaded {len(documents)} wiki documents")
        return documents
    except Exception as e:
        print(f"❌ Error loading wiki docs: {e}")
        return []


def init_chat_interface():
    """Initialize the RAG query engine."""
    global query_engine, chat_history
    
    try:
        print("🔄 Initializing RAG system...")
        
        # Initialize LLM settings
        llm = Ollama(model=LLM_MODEL, base_url=BASE_URL, request_timeout=300.0)
        embed_model = OllamaEmbedding(model_name=EMBED_MODEL, base_url=BASE_URL)
        
        Settings.llm = llm
        Settings.embed_model = embed_model
        Settings.node_parser = SimpleNodeParser.from_defaults(chunk_size=700, chunk_overlap=80)
        
        # Load wiki markdown documents
        print("📚 Loading company wiki documents...")
        wiki_docs = load_wiki_markdown_docs(DEFAULT_WIKI_DIR)
        
        if not wiki_docs:
            print("❌ No documents found!")
            return False
        
        print("🗂️ Setting up vector store...")
        chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        vector_store = ChromaVectorStore(
            chroma_collection=chroma_client.get_or_create_collection(COLLECTION_NAME)
        )
        
        index = VectorStoreIndex.from_documents(
            wiki_docs, vector_store=vector_store, show_progress=True
        )
        
        # Setup query engine
        retriever = VectorIndexRetriever(index=index, similarity_top_k=2)
        query_engine = RetrieverQueryEngine(retriever=retriever, llm=llm)
        
        print("✅ RAG system ready!")
        chat_history = []
        return True
        
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        return False


def chat(message: str, history):
    """Process user message and return assistant response."""
    global query_engine, chat_history
    
    if query_engine is None:
        return "⚠️ System not initialized. Please refresh the page."
    
    try:
        print(f"🔍 Query: {message}")
        response = query_engine.query(message)
        
        answer = str(response)
        
        # Extract source info
        sources = []
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes[:2]:
                if node.metadata.get('source'):
                    sources.append(node.metadata['source'])
        
        # Format response
        if sources:
            answer += f"\n\n📚 **Sources:**\n"
            for i, src in enumerate(sources, 1):
                answer += f"- {src}\n"
        
        print(f"✅ Response sent")
        return answer
        
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return f"❌ Error: {str(e)}"


def main():
    """Build and launch Gradio interface."""
    print("🚀 Starting Gradio Chat Interface...")
    
    # Initialize system
    if not init_chat_interface():
        print("❌ Failed to initialize RAG system")
        sys.exit(1)
    
    # Create Gradio interface
    with gr.Blocks(title="Wyrd RAG Chat", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🧠 Wyrd Support & Wiki Q&A")
        gr.Markdown("Ask questions about support tickets and company wiki. The system will retrieve relevant information and provide answers.")
        
        chatbot = gr.ChatInterface(
            chat,
            examples=[
                "What is Wyrd and what do we stand for?",
                "How do we fight against our enemies?",
                "What is our company doctrine?",
                "How are we built as a company?",
                "Who are we for and who are we fighting against?"
            ],
            title="Ask About Wyrd",
            description="Ask questions about Wyrd company, culture, and values"
        )
    
    # Launch
    print("🌐 Opening browser at http://localhost:7860")
    demo.launch(
        server_name="localhost",
        server_port=7860,
        share=False,
        show_api=False
    )


if __name__ == "__main__":
    main()
