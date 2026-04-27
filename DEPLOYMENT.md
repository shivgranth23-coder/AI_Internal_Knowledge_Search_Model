# 🚀 Deployment & Getting Started Guide

## ⚡ 5-Minute Setup

### For Windows Users

```powershell
# 1. Clone repository
git clone <your-repo>
cd Internal_Project_knoweldge_Search

# 2. Run setup script
python setup.py

# 3. Start Ollama (Terminal 1)
ollama serve

# 4. Start Backend (Terminal 2)
.\venv\Scripts\activate.ps1
python backend/main.py

# 5. Start Frontend (Terminal 3)
cd frontend
npm start
```

**Browser opens to:** `http://localhost:3000` ✅

---

### For Mac/Linux Users

```bash
# 1. Clone repository
git clone <your-repo>
cd Internal_Project_knoweldge_Search

# 2. Run setup script
python3 setup.py

# 3. Start Ollama (Terminal 1)
ollama serve

# 4. Start Backend (Terminal 2)
source venv/bin/activate
python backend/main.py

# 5. Start Frontend (Terminal 3)
cd frontend
npm start
```

**Browser opens to:** `http://localhost:3000` ✅

---

## 📦 Manual Setup (If Setup Script Fails)

### Step 1: Python Environment
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate.ps1

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Frontend Setup
```bash
cd frontend
npm install
```

### Step 3: Get Ollama
- Download: https://ollama.ai
- Install and run: `ollama serve`
- Download model: `ollama pull phi` (or your preferred model)

### Step 4: Start Services

**Terminal 1 - Backend:**
```bash
python backend/main.py
# Wait for: "Uvicorn running on http://0.0.0.0:8000"
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# Browser opens automatically to http://localhost:3000
```

**Terminal 3 - Ollama:**
```bash
ollama serve
# Keep running in background
```

---

## 🎯 Using the Application

### First Time Setup
1. **Upload PDFs**
   - Click "Choose Files" in the UI
   - Select your PDF documents
   - Click "Upload"

2. **Index Documents**
   - Click "Index Documents" button
   - Wait for completion (shows number of chunks created)
   - This creates searchable embeddings

3. **Ask Questions**
   - Type your question in the search box
   - Click "Search"
   - Wait 30-40 seconds for AI answer
   - View sources where answer came from

### Example Queries
- "What is the main topic of these documents?"
- "Summarize the key points"
- "What are the financial details mentioned?"
- "Who are the key people mentioned?"
- "What are the main findings?"

---

## 🔧 Configuration

### Change AI Model
Edit `backend/main.py`, line 27:
```python
# Current (fast):
llm_caller = OllamaLLMCaller(model="phi")

# Better quality (slower):
llm_caller = OllamaLLMCaller(model="mistral")
```

Available models:
- `phi` - Fastest (640MB)
- `orca-mini` - Fast (1.3GB)
- `neural-chat` - Medium (2.3GB)
- `mistral` - Best (4.4GB)

### Adjust Answer Length
Edit `backend/main.py`, line 32:
```python
class SearchRequest(BaseModel):
    max_tokens: int = 30  # Increase for longer answers (30-100)
```

### Change Embedding Model
Edit `backend/embedding.py`, line 11:
```python
def __init__(self, db_path: str = "./data/chroma_db", 
             model_name: str = "all-MiniLM-L6-v2"):
    # Other options: "paraphrase-MiniLM-L6-v2", "all-mpnet-base-v2"
```

---

## 🐛 Troubleshooting

### "Can't connect to localhost:3000"
✅ **Solution:** Start frontend with `npm start` in frontend folder

### "HTTP 500 - LLM error"
✅ **Solution:** 
- Check if Ollama is running: `ollama serve`
- Download model: `ollama pull phi`

### "Request timeout"
✅ **Solution:**
- Use faster model: `ollama pull phi`
- Reduce tokens: Change `max_tokens` to 20
- Close other applications to free memory

### "No documents in database"
✅ **Solution:**
- Click "Index Documents" button
- Make sure PDFs are in `documents/` folder
- Wait for indexing to complete

### "npm command not found"
✅ **Solution:**
- Install Node.js: https://nodejs.org
- Restart terminal after installing

### "Python module not found"
✅ **Solution:**
```bash
# Activate virtual environment
.\venv\Scripts\activate.ps1  # Windows
source venv/bin/activate     # Mac/Linux

# Install missing packages
pip install -r requirements.txt
```

---

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.10+ |
| Node.js | 14 | 16+ |
| RAM | 3GB | 8GB |
| Disk | 5GB | 20GB |
| Model | phi (640MB) | neural-chat (2.3GB) |

---

## 🔍 Testing Your Setup

### Test 1: Ollama Connection
```powershell
python test_ollama.py
```
All 3 checks should pass ✓

### Test 2: Backend Pipeline
```powershell
python test_backend.py
```
Should test embedding, search, and RAG

### Test 3: API
```powershell
curl http://localhost:8000/health
```
Should return status info

---

## 📝 Project Files

```
├── README.md                    # Main documentation
├── DEPLOYMENT.md               # This file
├── setup.py                    # Automated setup script
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
│
├── backend/
│   ├── main.py                # FastAPI server (port 8000)
│   ├── embedding.py           # Vector database integration
│   ├── llm_caller.py          # Ollama API integration
│   ├── pdf_processor.py       # PDF processing
│   └── __init__.py
│
├── frontend/
│   ├── package.json           # npm dependencies
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css
│   │   ├── index.js           # Entry point
│   │   └── components/
│   │       ├── SearchBox.js   # Search input
│   │       ├── ResultDisplay.js
│   │       └── StatusBar.js
│   └── public/
│       └── index.html         # HTML template
│
├── documents/                 # Your PDFs go here
├── data/                      # Database storage
└── test_*.py                  # Diagnostic scripts
```

---

## 💾 Backing Up Your Data

### Save Indexed Documents
```bash
# Database location
./data/chroma_db

# PDFs location
./documents/
```

### Export Database
```bash
# Backup command (in development)
tar -czf backup_$(date +%Y%m%d).tar.gz data/ documents/
```

---

## 🌐 Network Access

### Local Network (Same WiFi)
1. Find your IP: `ipconfig getifaddr en0` (Mac) or `ipconfig` (Windows)
2. Access from other device: `http://<YOUR_IP>:3000`

### Remote Access
- Use VPN or port forwarding (advanced)
- Or deploy to cloud (Docker, AWS, Heroku)

---

## 🐳 Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "backend/main.py"]
```

```bash
docker build -t pdf-search .
docker run -p 8000:8000 pdf-search
```

---

## 📈 Performance Tips

1. **Faster Answers**
   - Use `phi` model instead of `mistral`
   - Reduce `max_tokens` to 20-30
   - Keep documents < 100MB total

2. **Better Answers**
   - Use `mistral` model
   - Increase `max_tokens` to 50-100
   - Add more relevant context

3. **Lower Memory Usage**
   - Use `phi` model (640MB)
   - Close other applications
   - Reduce `top_k` in search (current: 2)

---

## 🚀 Production Considerations

- Enable authentication
- Add rate limiting
- Use HTTPS
- Set up monitoring
- Add API versioning
- Implement caching
- Use load balancing

---

## 📞 Support & Help

1. **Check README.md** - Comprehensive documentation
2. **Run diagnostics** - `python test_backend.py`
3. **Check API docs** - `http://localhost:8000/docs`
4. **Review logs** - Check terminal output for errors

---

## ✅ Checklist Before Committing to GitHub

- [ ] All dependencies in requirements.txt
- [ ] .gitignore configured properly
- [ ] README.md with clear instructions
- [ ] DEPLOYMENT.md with setup guide
- [ ] setup.py for automated setup
- [ ] Test scripts working
- [ ] No API keys or secrets in code
- [ ] documents/ folder has .gitkeep
- [ ] data/ folder has .gitkeep
- [ ] Examples or sample queries provided

---

**Happy deploying! 🎉**
