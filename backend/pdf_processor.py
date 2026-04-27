"""PDF extraction and chunking module."""
import os
from typing import List, Dict
import pdfplumber


class PDFProcessor:
    """Extract and chunk PDF documents."""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize PDF processor.
        
        Args:
            chunk_size: Number of tokens per chunk (approximate)
            overlap: Number of tokens to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text from PDF with metadata.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with text content and metadata
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                pages = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num} ---\n{page_text}"
                
                return {
                    "filename": os.path.basename(pdf_path),
                    "filepath": pdf_path,
                    "text": text,
                    "pages": pages,
                    "success": True
                }
        except Exception as e:
            return {
                "filename": os.path.basename(pdf_path),
                "filepath": pdf_path,
                "text": "",
                "pages": 0,
                "success": False,
                "error": str(e)
            }

    def chunk_text(self, text: str, metadata: Dict) -> List[Dict[str, str]]:
        """
        Split text into chunks with overlap.
        
        Args:
            text: Full text content
            metadata: Document metadata (filename, etc)
            
        Returns:
            List of chunks with metadata
        """
        # Simple word-based chunking (approximate token count)
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            if chunk_text.strip():
                chunks.append({
                    "content": chunk_text,
                    "source": metadata.get("filename", "unknown"),
                    "filepath": metadata.get("filepath", ""),
                    "chunk_index": len(chunks)
                })
        
        return chunks

    def process_pdf_directory(self, directory: str) -> List[Dict]:
        """
        Process all PDFs in a directory.
        
        Args:
            directory: Path to directory containing PDFs
            
        Returns:
            List of all chunks from all PDFs
        """
        all_chunks = []
        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(directory, pdf_file)
            print(f"Processing: {pdf_file}")
            
            # Extract text
            extraction_result = self.extract_text_from_pdf(pdf_path)
            
            if not extraction_result["success"]:
                print(f"  ✗ Failed to extract: {extraction_result.get('error')}")
                continue
            
            # Chunk text
            chunks = self.chunk_text(
                extraction_result["text"],
                extraction_result
            )
            
            all_chunks.extend(chunks)
            print(f"  ✓ Processed {len(chunks)} chunks from {extraction_result['pages']} pages")
        
        return all_chunks
