"""Ollama LLM integration module."""
import requests
from typing import List, Dict
import json


class OllamaLLMCaller:
    """Interface to Ollama local LLM."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        """
        Initialize Ollama LLM caller.
        
        Args:
            base_url: Ollama API base URL
            model: Model name to use (must be pulled in Ollama first)
        """
        self.base_url = base_url
        self.model = model
        self.api_endpoint = f"{base_url}/api/generate"

    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            return False

    def generate_answer(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 30
    ) -> Dict[str, str]:
        """
        Generate answer using Ollama.
        
        Args:
            prompt: Input prompt
            temperature: Model temperature (0.0 - 2.0)
            max_tokens: Maximum tokens to generate (default 50 for speed)
            
        Returns:
            Dictionary with generated response and metadata
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "num_predict": max_tokens
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=180
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "model": self.model,
                    "total_duration": result.get("total_duration", 0),
                    "load_duration": result.get("load_duration", 0),
                    "prompt_eval_count": result.get("prompt_eval_count", 0),
                    "eval_count": result.get("eval_count", 0)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response": ""
                }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout - model may be busy or not responding",
                "response": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": ""
            }

    def create_rag_prompt(
        self,
        query: str,
        context_chunks: List[str],
        system_instruction: str = None
    ) -> str:
        """
        Create a simplified RAG prompt combining query and context.
        
        Args:
            query: User query
            context_chunks: Relevant document chunks
            system_instruction: Optional system instruction
            
        Returns:
            Formatted prompt string
        """
        # Limit to first 2 chunks only and truncate each to 500 chars
        limited_chunks = context_chunks[:2]
        truncated = [chunk[:500] for chunk in limited_chunks]
        
        context = "\n---\n".join(truncated)
        
        prompt = f"""Based on the following information, answer the question concisely in 1-2 sentences.

Information:
{context}

Question: {query}

Answer:"""
        return prompt
