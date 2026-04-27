# 📚 PDF Knowledge Search - AI-Powered Document QA System

An intelligent application that lets you upload PDF documents and ask questions about them using AI. Powered by FastAPI, React, Chroma, and Ollama - completely offline and privacy-focused.

## 🎯 Features

- **Semantic Search**: Smart search that understands meaning, not just keywords
- **RAG Pipeline**: Retrieves relevant document chunks and generates contextual answers
- **Local LLM**: Uses Ollama for private, offline LLM inference
- **Web GUI**: Beautiful, responsive React-based user interface
- **Vector Database**: Chroma for fast semantic similarity search
- **Source Citations**: Know exactly which documents your answers came from

## 📋 Project Structure

```
Internal_Project_knoweldge_Search/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI app & RAG endpoints
│   ├── pdf_processor.py       # PDF extraction & chunking
│   ├── embedding.py           # Vector database & embeddings
│   └── llm_caller.py          # Ollama integration
├── frontend/                   # React GUI
│   ├── public/                # Static files
│   ├── src/                   # React components
│   └── package.json           # Frontend dependencies
├── documents/                  # Your PDF files (to be indexed)
├── data/                       # Vector database storage
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+ (for frontend)
- Ollama installed locally ([download here](https://ollama.ai))

### Step 1: Install Backend Dependencies

```bash
cd Internal_Project_knoweldge_Search
python -m venv venv
venv\Scripts\activate  # On Windows
# or: source venv/bin/activate  # On Linux/Mac

pip install -r requirements.txt
```

### Step 2: Set Up Ollama

```bash
# Download and start Ollama
ollama serve

# In another terminal, pull a model (first time only)
ollama pull mistral
# or: ollama pull neural-chat  (lightweight alternative)
```

### Step 3: Organize Your Documents

1. Copy all your PDF files to the `documents/` folder
2. The system will automatically index them when you start

### Step 4: Start the Backend

```bash
cd backend
python main.py
```

Backend will be available at: `http://localhost:8000`

### Step 5: Start the Frontend (in another terminal)

```bash
cd frontend
npm install  # First time only
npm start
```

Frontend will be available at: `http://localhost:3000`

## 📖 Usage

1. **Index Documents**:
   - Click the "Index Documents" button in the GUI
   - Wait for confirmation (shows number of chunks created)

2. **Ask Questions**:
   - Type your question in the search box
   - Press "Search" or Enter
   - Get AI-generated answers with source citations

3. **Example Questions**:
   - "What are the key concepts in product management?"
   - "Summarize the AI-enhanced product framework"
   - "What strategies are mentioned for go-to-market?"

## 🔧 Configuration

### Backend Settings (backend/main.py)

- **LLM Model**: Change `model="mistral"` to use different Ollama models
- **Document Directory**: Modify `DOCUMENTS_DIR` path
- **Database Path**: Adjust `db_path="./data/chroma_db"`

### Search Parameters

- **top_k**: Number of document chunks to retrieve (default: 5)
- **temperature**: LLM creativity (0.0 = deterministic, 2.0 = very creative)
- **max_tokens**: Maximum answer length

### Ollama Model Options

Lightweight (faster):
```bash
ollama pull neural-chat
ollama pull orca-mini
```

Balanced (recommended):
```bash
ollama pull mistral
ollama pull llama2-uncensored
```

Powerful (slower):
```bash
ollama pull neural-chat:13b
ollama pull mistral:13b
```

## 📊 How It Works

```
User Question
    ↓
Semantic Search in Vector DB
    ↓
Retrieve Top-K Relevant Chunks
    ↓
Create RAG Prompt
    ↓
Send to Ollama LLM
    ↓
Generate Answer with Context
    ↓
Display with Source Citations
```

## 🔍 API Endpoints

### Health Check
```
GET /health
```

### Index Documents
```
POST /index
```

### Search
```
POST /search
{
  "query": "Your question here",
  "top_k": 5,
  "temperature": 0.7,
  "max_tokens": 500
}
```

### System Status
```
GET /status
```

## 🛠️ Troubleshooting

### "Ollama is not running" error
- Make sure Ollama is running: `ollama serve`
- Default URL is `http://localhost:11434`

### Backend API not connecting
- Verify backend is running: `python main.py` in backend folder
- Check API at `http://localhost:8000/docs`

### Poor search results
- Ensure PDFs are indexed: Click "Index Documents" button
- Try different chunk sizes in `pdf_processor.py`
- Use a more capable model (e.g., `mistral` vs `neural-chat`)

### Slow performance
- Use a smaller model: `ollama pull neural-chat`
- Reduce `top_k` in search parameters
- Increase `max_tokens` may slow down generation

### Out of Memory
- Close other applications
- Use a smaller Ollama model
- Reduce chunk size in `pdf_processor.py`

## 📦 Dependencies

### Backend
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **pdfplumber**: PDF extraction
- **sentence-transformers**: Embeddings
- **chromadb**: Vector database
- **ollama**: LLM integration
- **requests**: HTTP client

### Frontend
- **React**: UI framework
- **Axios**: HTTP client

## 🚀 Advanced Usage

### Custom Embedding Model

In `backend/embedding.py`:
```python
self.model = SentenceTransformer("all-mpnet-base-v2")  # More accurate but slower
```

Other options:
- `"all-MiniLM-L6-v2"` (current, fast)
- `"all-mpnet-base-v2"` (slower, more accurate)
- `"paraphrase-MiniLM-L6-v2"` (good for questions)

### Re-index Documents

```bash
# Clear database and re-index
curl -X POST http://localhost:8000/index
```

### Custom Document Processing

Modify `pdf_processor.py` to handle:
- OCR for scanned PDFs
- Different chunking strategies
- Custom metadata extraction

## 📝 Performance Tips

1. **Embedding Model**: Smaller models (MiniLM) faster but less accurate
2. **Chunk Size**: Larger chunks = fewer searches, smaller = more precise
3. **Vector Search**: Cosine similarity is fast and effective
4. **LLM Model**: Smaller Ollama models (7B) run faster than larger ones (13B+)

## 🔐 Security Notes

- PDFs are processed locally; no data sent to cloud
- Ollama runs on localhost (not exposed to internet by default)
- Vector database stored locally in `data/` folder

## 📄 License

Internal Use Only

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all services are running (Backend, Ollama, Frontend)
3. Check logs in backend terminal
4. Ensure PDFs are in `documents/` folder

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [RAG Concepts](https://arxiv.org/abs/2005.11401)

---

**Created by**: Shivkant Chakravarti
**Created**: April 2026
**Last Updated**: April 25, 2026
**License**: Internal Use Only
