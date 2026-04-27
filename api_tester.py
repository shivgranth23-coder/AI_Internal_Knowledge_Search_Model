"""
Simple API Tester - Test backend without GUI or npm
Run this after backend is running to test everything
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")

def test_health():
    """Test if backend is running"""
    print_header("Testing Backend Connection")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print("✅ Backend is running!")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Ollama Connected: {data.get('ollama_connected')}")
        print(f"Database Documents: {data.get('database_documents')}")
        return True
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        print("   Make sure: python main.py is running in backend folder")
        return False

def test_status():
    """Get system status"""
    print_header("System Status")
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=5)
        data = response.json()
        print(json.dumps(data, indent=2))
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_index():
    """Index PDFs"""
    print_header("Indexing Documents")
    try:
        print("Starting indexing... this may take 2-5 minutes...\n")
        response = requests.post(f"{BASE_URL}/index", timeout=300)
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Indexing successful!")
            print(f"   Documents processed: {data.get('documents_processed')}")
            print(f"   Chunks created: {data.get('chunks_created')}")
        else:
            print(f"❌ Indexing failed: {data.get('error')}")
        return data.get('success', False)
    except requests.exceptions.Timeout:
        print("⏱️ Indexing is taking a while... it's still running")
        print("   This is normal for first time - please wait...")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search(query="What is product management?"):
    """Test search"""
    print_header(f"Testing Search")
    print(f"Query: {query}\n")
    try:
        response = requests.post(
            f"{BASE_URL}/search",
            json={
                "query": query,
                "top_k": 5,
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=120
        )
        data = response.json()
        
        if data.get('success'):
            print("✅ Search successful!\n")
            print(f"Answer:\n{data.get('answer')}\n")
            
            sources = data.get('sources', [])
            if sources:
                print(f"Sources ({len(sources)}):")
                for source in sources:
                    print(f"  • {source.get('source')}")
        else:
            print(f"❌ Search failed: {data.get('error')}")
            print("\nCommon causes:")
            print("  • Ollama not running")
            print("  • Model not downloaded (run: ollama pull mistral)")
            print("  • PDFs not indexed yet")
        
        return data.get('success', False)
    except requests.exceptions.Timeout:
        print("⏱️ Search is taking a while...")
        print("   First search loads the model, may take 30-60 seconds")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  PDF Knowledge Search - API Tester".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    print("\n📋 Testing sequence:")
    print("  1. Health check")
    print("  2. System status")
    print("  3. Index documents (if needed)")
    print("  4. Test search")
    
    # Test health
    if not test_health():
        print("\n❌ Cannot continue - backend not running")
        print("   Start it: python main.py (in backend folder)")
        return
    
    # Test status
    time.sleep(1)
    test_status()
    
    # Ask about indexing
    time.sleep(1)
    print_header("Ready to Index?")
    print("This processes all PDFs and may take 2-5 minutes")
    user_input = input("Index documents now? (yes/no): ").strip().lower()
    
    if user_input in ['yes', 'y']:
        indexed = test_index()
    else:
        indexed = False
        print("⏭️ Skipping indexing")
    
    # Test search if indexed
    time.sleep(1)
    if indexed:
        print_header("Ready to Search?")
        user_query = input("Enter your question (or press Enter for default): ").strip()
        if not user_query:
            user_query = "What is product management?"
        
        test_search(user_query)
    else:
        print("\n⚠️ Cannot search - documents not indexed")
        print("   Run indexing first with /index endpoint")
    
    print("\n" + "="*60)
    print("Testing complete!")
    print("="*60)
    print("\nNext steps:")
    print("  • Keep backend running (Ctrl+C to stop)")
    print("  • Install Node.js and npm for web GUI")
    print("  • Or use http://localhost:8000/docs for API testing")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
