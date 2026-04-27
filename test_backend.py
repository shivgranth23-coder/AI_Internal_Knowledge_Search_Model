#!/usr/bin/env python3
"""
Diagnostic test for backend components
Tests embedding, database, and search pipeline
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from embedding import EmbeddingManager
from llm_caller import OllamaLLMCaller
import time

def test_embedding_database():
    """Test embedding manager and database"""
    print("\n" + "="*60)
    print("  1. Testing Embedding & Database")
    print("="*60)
    
    try:
        print("\n[*] Initializing embedding manager...")
        embedding_manager = EmbeddingManager(db_path="./data/chroma_db")
        
        stats = embedding_manager.get_stats()
        print(f"    Database documents: {stats['total_documents']}")
        print(f"    Embedding dimension: {stats['model']}")
        
        if stats['total_documents'] == 0:
            print("\n    ✗ WARNING: No documents in database!")
            print("      Please run: http://localhost:8000/index")
            return False
        else:
            print(f"\n    ✓ {stats['total_documents']} documents found!")
            return True
            
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

def test_search_speed(embedding_manager):
    """Test how fast search works"""
    print("\n" + "="*60)
    print("  2. Testing Search Speed")
    print("="*60)
    
    try:
        query = "test query"
        
        print(f"\n[*] Searching for: '{query}'...")
        start = time.time()
        results = embedding_manager.search(query, top_k=3)
        elapsed = time.time() - start
        
        print(f"    ✓ Search completed in {elapsed:.2f}s")
        print(f"    Results found: {len(results)}")
        
        if elapsed > 10:
            print(f"    ⚠ WARNING: Search is slow ({elapsed:.2f}s)")
            print("      This might cause timeouts in the API")
        
        return True
        
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

def test_rag_pipeline(embedding_manager, llm_caller):
    """Test the full RAG pipeline"""
    print("\n" + "="*60)
    print("  3. Testing RAG Pipeline")
    print("="*60)
    
    try:
        query = "What is this document about?"
        
        # Step 1: Search
        print(f"\n[*] Step 1: Searching for relevant chunks...")
        start = time.time()
        relevant_docs = embedding_manager.search(query, top_k=3)
        search_time = time.time() - start
        
        if not relevant_docs:
            print(f"    ✗ No documents found!")
            return False
        
        print(f"    ✓ Found {len(relevant_docs)} chunks in {search_time:.2f}s")
        
        # Step 2: Create RAG prompt
        print(f"\n[*] Step 2: Creating RAG prompt...")
        context_chunks = [doc["content"] for doc in relevant_docs]
        rag_prompt = llm_caller.create_rag_prompt(query, context_chunks)
        print(f"    ✓ Prompt created ({len(rag_prompt)} chars)")
        
        # Step 3: Generate answer
        print(f"\n[*] Step 3: Generating answer with LLM...")
        print(f"    (This may take 10-30 seconds...)")
        start = time.time()
        
        llm_result = llm_caller.generate_answer(
            rag_prompt,
            temperature=0.7,
            max_tokens=100
        )
        llm_time = time.time() - start
        
        if llm_result["success"]:
            print(f"    ✓ Answer generated in {llm_time:.2f}s")
            print(f"    Answer: {llm_result['response'][:100]}...")
            return True
        else:
            print(f"    ✗ LLM error: {llm_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

def main():
    """Run all diagnostics"""
    print("\n" + "="*60)
    print("  Backend Diagnostic Test")
    print("="*60)
    
    # Test embedding and database
    if not test_embedding_database():
        print("\n✗ Database test failed!")
        return False
    
    # Initialize managers
    embedding_manager = EmbeddingManager(db_path="./data/chroma_db")
    llm_caller = OllamaLLMCaller(base_url="http://localhost:11434", model="phi")
    
    # Test search speed
    if not test_search_speed(embedding_manager):
        print("\n✗ Search speed test failed!")
        return False
    
    # Test RAG pipeline
    if not test_rag_pipeline(embedding_manager, llm_caller):
        print("\n✗ RAG pipeline test failed!")
        return False
    
    print("\n" + "="*60)
    print("  ✓ All tests passed! System should work.")
    print("="*60 + "\n")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted!")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
