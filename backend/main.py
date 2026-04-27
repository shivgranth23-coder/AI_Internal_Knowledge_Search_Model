"""FastAPI backend for PDF knowledge search with RAG."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os
from pathlib import Path

from pdf_processor import PDFProcessor
from embedding import EmbeddingManager
from llm_caller import OllamaLLMCaller


# Initialize FastAPI app
app = FastAPI(title="PDF Knowledge Search API", version="1.0.0")

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
pdf_processor = PDFProcessor(chunk_size=500, overlap=50)
embedding_manager = EmbeddingManager(db_path="./data/chroma_db")
llm_caller = OllamaLLMCaller(base_url="http://localhost:11434", model="phi")

# Configuration
DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)


# Request/Response models
class SearchRequest(BaseModel):
    """Search request model."""
    query: str
    top_k: int = 2
    temperature: float = 0.7
    max_tokens: int = 30


class SearchResponse(BaseModel):
    """Search response model."""
    query: str
    answer: str
    sources: List[Dict[str, str]]
    metadata: Dict
    success: bool
    error: str = None


class IndexingResponse(BaseModel):
    """Indexing response model."""
    success: bool
    documents_processed: int
    chunks_created: int
    error: str = None


# Routes

@app.get("/health")
def health_check():
    """Health check endpoint."""
    ollama_connected = llm_caller.check_connection()
    db_stats = embedding_manager.get_stats()
    
    return {
        "status": "healthy",
        "ollama_connected": ollama_connected,
        "database_documents": db_stats["total_documents"]
    }


@app.post("/index", response_model=IndexingResponse)
def index_documents():
    """Index all PDF documents in the documents directory."""
    try:
        if not os.path.exists(DOCUMENTS_DIR):
            raise Exception(f"Documents directory not found: {DOCUMENTS_DIR}")
        
        # Process all PDFs
        chunks = pdf_processor.process_pdf_directory(DOCUMENTS_DIR)
        
        if not chunks:
            raise Exception("No PDF chunks were extracted")
        
        # Clear old database
        embedding_manager.reset_database()
        
        # Add to vector database
        num_added = embedding_manager.add_documents(chunks)
        
        return IndexingResponse(
            success=True,
            documents_processed=len(os.listdir(DOCUMENTS_DIR)),
            chunks_created=num_added
        )
    except Exception as e:
        return IndexingResponse(
            success=False,
            documents_processed=0,
            chunks_created=0,
            error=str(e)
        )


@app.post("/search", response_model=SearchResponse)
def search_knowledge(request: SearchRequest):
    """
    Search PDFs and generate answer using RAG.
    
    Args:
        request: Search request with query and parameters
        
    Returns:
        SearchResponse with answer and sources
    """
    try:
        # Check Ollama connection
        if not llm_caller.check_connection():
            raise Exception("Ollama is not running. Please start Ollama with: ollama serve")
        
        # Search for relevant chunks
        relevant_docs = embedding_manager.search(request.query, top_k=request.top_k)
        
        if not relevant_docs:
            return SearchResponse(
                query=request.query,
                answer="No relevant information found in the documents.",
                sources=[],
                metadata={},
                success=True
            )
        
        # Extract content for RAG
        context_chunks = [doc["content"] for doc in relevant_docs]
        
        # Create RAG prompt
        rag_prompt = llm_caller.create_rag_prompt(request.query, context_chunks)
        
        # Generate answer
        llm_result = llm_caller.generate_answer(
            rag_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        if not llm_result["success"]:
            raise Exception(f"LLM error: {llm_result.get('error')}")
        
        # Format sources
        sources = [
            {
                "source": doc["source"],
                "filepath": doc["filepath"],
                "chunk_index": doc["chunk_index"]
            }
            for doc in relevant_docs
        ]
        
        return SearchResponse(
            query=request.query,
            answer=llm_result["response"].strip(),
            sources=sources,
            metadata={
                "model": llm_result.get("model"),
                "prompt_tokens": llm_result.get("prompt_eval_count"),
                "response_tokens": llm_result.get("eval_count")
            },
            success=True
        )
    except Exception as e:
        return SearchResponse(
            query=request.query,
            answer="",
            sources=[],
            metadata={},
            success=False,
            error=str(e)
        )


@app.get("/status")
def get_status():
    """Get system status and database information."""
    db_stats = embedding_manager.get_stats()
    ollama_connected = llm_caller.check_connection()
    
    return {
        "database": {
            "total_documents": db_stats["total_documents"],
            "embedding_dimension": db_stats["model"]
        },
        "ollama": {
            "connected": ollama_connected,
            "model": llm_caller.model,
            "url": llm_caller.base_url
        },
        "documents_directory": DOCUMENTS_DIR
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("PDF Knowledge Search API - Starting...")
    print("=" * 60)
    print(f"Documents directory: {DOCUMENTS_DIR}")
    print("API will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
