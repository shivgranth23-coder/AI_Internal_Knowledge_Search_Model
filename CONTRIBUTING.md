# CONTRIBUTING

Thank you for your interest in contributing to PDF Knowledge Search!

## 🛠️ Development Setup

### Clone & Setup
```bash
git clone <your-fork>
cd Internal_Project_knoweldge_Search
python setup.py
```

### Branch Naming
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring

Example: `git checkout -b feature/add-authentication`

## 📝 Code Style

### Python
- Use `black` for formatting
- Follow PEP 8
- Type hints required
- Docstrings for functions

```bash
pip install black
black backend/
```

### JavaScript/React
- Use `prettier` for formatting
- Follow ESLint rules
- Functional components
- Hooks preferred

```bash
npm install -D prettier eslint
npm run format
```

## 🧪 Testing

### Python Tests
```bash
python -m pytest backend/
python test_backend.py
python test_ollama.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📤 Committing Changes

### Commit Message Format
```
[TYPE] Brief description

Optional detailed explanation

Fixes #issue_number
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
[feat] Add authentication to API

- Implement JWT token validation
- Add login endpoint
- Protect search endpoint

Fixes #42
```

### Before Pushing
```bash
# 1. Format code
black backend/
npm run format

# 2. Run tests
python test_backend.py
npm test

# 3. Check git status
git status

# 4. Commit
git add .
git commit -m "[feat] Your message"

# 5. Push
git push origin your-branch
```

## 🔄 Pull Request Process

1. **Create Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Follow code style
   - Add tests
   - Update docs

3. **Test Locally**
   ```bash
   python test_backend.py
   python backend/main.py  # Check no errors
   npm start  # Check frontend works
   ```

4. **Push & Create PR**
   ```bash
   git push origin feature/your-feature
   ```
   
5. **PR Description**
   - What does this change?
   - Why is it needed?
   - Any breaking changes?

## 🐛 Bug Reports

Include:
- Python/Node version
- OS (Windows/Mac/Linux)
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Screenshots if relevant

## 💡 Feature Requests

Describe:
- Problem being solved
- Proposed solution
- Alternative approaches
- Use cases/examples

## 📚 Documentation

### Update README.md
- Keep accurate
- Update when features change
- Include examples

### Code Comments
```python
# Good
def search_documents(query: str) -> List[Dict]:
    """Search indexed documents using semantic similarity."""
    # Embed query using the same model as database
    query_embedding = self.model.encode([query])[0]
    
    # Search in vector database
    results = self.collection.query(...)
    return results

# Avoid
def search_documents(query):
    # search function
    x = self.model.encode([query])[0]
    y = self.collection.query(...)
    return y
```

## 🚀 Performance Tips

### For Backend
- Cache embeddings
- Batch process requests
- Use async/await where applicable
- Monitor memory usage

### For Frontend
- Use React.memo for expensive components
- Implement pagination
- Lazy load images
- Optimize bundle size

## 🔒 Security

- Never commit API keys or secrets
- Use environment variables
- Validate all inputs
- Sanitize user data
- Don't hardcode credentials
- Use HTTPS in production

## 📦 Deployment

New features should include:
- [ ] Backend code
- [ ] Frontend code (if applicable)
- [ ] API documentation
- [ ] Tests
- [ ] Updated README
- [ ] DEPLOYMENT.md updates

## 🎯 Areas We Need Help

- [ ] Better error handling
- [ ] Performance optimization
- [ ] UI/UX improvements
- [ ] Documentation
- [ ] Tests
- [ ] Docker containerization
- [ ] Authentication
- [ ] Advanced RAG features

## ❓ Questions?

- Open an issue
- Check existing docs
- Review similar PRs

## 📄 License

By contributing, you agree your code will be under MIT License.

---

**Thank you for contributing! 🙌**
