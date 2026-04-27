#!/usr/bin/env python3
"""
Test Ollama connection and model availability
"""

import requests
import json
import sys

def test_ollama():
    """Test Ollama connection and generate a sample response"""
    
    print("="*60)
    print("  Testing Ollama Connection and Model")
    print("="*60)
    
    base_url = "http://localhost:11434"
    model = "mistral"
    
    # Test 1: Check if Ollama is running
    print("\n[1] Checking if Ollama is running...")
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            print("    ✓ Ollama is running")
            models = response.json().get("models", [])
            print(f"    Available models: {len(models)}")
            for m in models:
                print(f"      - {m.get('name')}")
        else:
            print(f"    ✗ Ollama returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"    ✗ Cannot connect to {base_url}")
        print("    Ensure Ollama is running with: ollama serve")
        return False
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False
    
    # Test 2: Check if mistral model is available
    print(f"\n[2] Checking if '{model}' model is available...")
    if not any(m.get("name", "").startswith(model) for m in models):
        print(f"    ✗ Model '{model}' not found")
        print(f"    Download it with: ollama pull {model}")
        return False
    print(f"    ✓ Model '{model}' is available")
    
    # Test 3: Try to generate a response
    print("\n[3] Testing model generation...")
    try:
        payload = {
            "model": model,
            "prompt": "What is 2+2? Answer in one sentence.",
            "stream": False,
            "temperature": 0.7
        }
        
        print(f"    Sending request to {base_url}/api/generate...")
        response = requests.post(
            f"{base_url}/api/generate",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("response", "").strip()
            print(f"    ✓ Model responded successfully")
            print(f"    Response: {answer[:100]}...")
            print(f"    Total duration: {result.get('total_duration', 0) / 1e9:.2f}s")
            return True
        else:
            print(f"    ✗ Ollama returned status {response.status_code}")
            print(f"    Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"    ✗ Request timeout (model may be busy)")
        return False
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_ollama()
    
    print("\n" + "="*60)
    if success:
        print("  ✓ Ollama is working! Try the search again.")
    else:
        print("  ✗ Ollama has issues. Fix above and try again.")
    print("="*60 + "\n")
    
    sys.exit(0 if success else 1)
