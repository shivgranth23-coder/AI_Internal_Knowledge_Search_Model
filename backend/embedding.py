"""Embedding and vector database module using Chroma."""
import os
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    """Manage document embeddings and vector database."""

    def __init__(self, db_path: str = "./data/chroma_db", model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding manager.
        
        Args:
            db_path: Path to store Chroma database
            model_name: Sentence transformer model to use
        """
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
        
        # Initialize Chroma persistent client
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="pdf_documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embedding model
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def add_documents(self, chunks: List[Dict[str, str]]) -> int:
        """
        Add document chunks to vector database.
        
        Args:
            chunks: List of document chunks with metadata
            
        Returns:
            Number of documents added
        """
        if not chunks:
            print("No chunks to add")
            return 0
        
        # Extract content for embedding
        contents = [chunk["content"] for chunk in chunks]
        
        # Generate embeddings
        print(f"Generating embeddings for {len(contents)} chunks...")
        embeddings = self.model.encode(contents, show_progress_bar=True)
        
        # Prepare metadata
        ids = [f"doc_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "source": chunk.get("source", "unknown"),
                "filepath": chunk.get("filepath", ""),
                "chunk_index": str(chunk.get("chunk_index", 0))
            }
            for chunk in chunks
        ]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=contents,
            metadatas=metadatas
        )
        
        print(f"✓ Added {len(chunks)} documents to vector database")
        return len(chunks)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant documents with scores
        """
        # Embed query
        query_embedding = self.model.encode([query])[0]
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "content": doc,
                    "source": results["metadatas"][0][i]["source"],
                    "filepath": results["metadatas"][0][i]["filepath"],
                    "chunk_index": results["metadatas"][0][i]["chunk_index"],
                    "distance": results["distances"][0][i] if results["distances"] else None
                })
        
        return formatted_results

    def get_stats(self) -> Dict:
        """Get database statistics."""
        return {
            "total_documents": self.collection.count(),
            "model": self.model.get_sentence_embedding_dimension()
        }

    def reset_database(self):
        """Clear all documents from the database."""
        self.client.delete_collection(name="pdf_documents")
        self.collection = self.client.get_or_create_collection(
            name="pdf_documents",
            metadata={"hnsw:space": "cosine"}
        )
        print("✓ Database cleared")
