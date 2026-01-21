# 🤖 Jarvis AI Assistant

A personal AI assistant powered by a **self-hosted LLM** (via LM Studio) with **Pinecone vector database** for knowledge retrieval and a modern **chatbot UI**.

![Jarvis AI Assistant](screenshot.png)

---

## ✨ Features

- � **Self-hosted LLM** - Uses LM Studio's OpenAI-compatible API (Qwen2.5-Coder-7B or any model)
- 📚 **Knowledge Base** - Store and retrieve information using Pinecone vector database
- 💬 **Modern Chat UI** - Clean, responsive dark-themed web interface
- 🔄 **Conversation Memory** - Maintains context across messages in a session
- 🔍 **Semantic Search** - Find relevant knowledge using sentence embeddings
- ⚡ **Real-time Status** - Live connection status for LLM and vector database

---

## 📁 Project Structure

```
jarvis-assistant/
├── app.py              # Main Flask application & API endpoints
├── config.py           # Configuration settings (loaded from .env)
├── llm_client.py       # LLM client for LM Studio (OpenAI-compatible)
├── vector_db.py        # Pinecone vector database client
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (create from .env.example)
├── .env.example        # Example environment file
├── README.md           # This file
└── static/
    ├── index.html      # Chat UI HTML
    ├── styles.css      # Dark theme styling
    └── script.js       # Frontend JavaScript
```

---

## 🛠️ Prerequisites

### 1. LM Studio (Required)
- Download from: https://lmstudio.ai/
- Load a model (e.g., Qwen2.5-Coder-7B-Instruct)
- Start the local server (default: `http://localhost:1234`)

### 2. Pinecone Account (Optional - for Knowledge Base)
- Sign up at: https://www.pinecone.io/ (free tier available)
- Create an API key from the dashboard

### 3. Python 3.9+
- Download from: https://www.python.org/downloads/

---

## 🚀 Quick Start

### 1. Clone/Download the Project

```bash
cd jarvis-assistant
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and update the values:

```env
# LM Studio Settings
LLM_BASE_URL=http://localhost:1234/v1
LLM_MODEL=qwen2.5-coder-7b-instruct

# Pinecone Settings (optional)
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_INDEX_NAME=jarvis-knowledge

# Flask Settings
FLASK_DEBUG=False
FLASK_PORT=5000
```

### 5. Start the Application

```bash
python app.py
```

### 6. Open the Chat UI

Navigate to: **http://localhost:5000**

---

## 📖 Usage Guide

### 💬 Chat
1. Type your message in the input field
2. Press **Enter** or click the send button
3. Jarvis will respond using the LLM
4. Conversation history is maintained within the session

### 📚 Knowledge Base
1. Click **"Knowledge"** in the sidebar
2. **Add Knowledge**: Enter information you want Jarvis to remember
3. **Search Knowledge**: Query your stored information
4. When chatting, Jarvis automatically searches the knowledge base for context

### Example Knowledge Entries:
- Company policies and procedures
- Product documentation
- FAQ answers
- Technical specifications
- Personal notes and reminders

---

## 🔌 API Endpoints

### Chat
```http
POST /api/chat
Content-Type: application/json

{
    "message": "Your message here",
    "session_id": "optional-session-id",
    "use_knowledge": true
}
```

### Add Knowledge
```http
POST /api/knowledge
Content-Type: application/json

{
    "text": "Information to store",
    "metadata": {"source": "optional metadata"}
}
```

### Search Knowledge
```http
POST /api/knowledge/search
Content-Type: application/json

{
    "query": "search query",
    "top_k": 3
}
```

### Health Check
```http
GET /api/health
```

### Clear Session
```http
POST /api/session/clear
Content-Type: application/json

{
    "session_id": "session-id"
}
```

---

## ⚙️ Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_BASE_URL` | LM Studio API endpoint | `http://localhost:1234/v1` |
| `LLM_MODEL` | Model identifier | `qwen2.5-coder-7b-instruct` |
| `PINECONE_API_KEY` | Pinecone API key | (empty) |
| `PINECONE_INDEX_NAME` | Pinecone index name | `jarvis-knowledge` |
| `FLASK_DEBUG` | Enable Flask debug mode | `False` |
| `FLASK_PORT` | Server port | `5000` |

---

## 🔧 Troubleshooting

### LLM Not Connecting
- ✅ Ensure LM Studio is running and the server is started
- ✅ Check the `LLM_BASE_URL` in your `.env` file
- ✅ Verify a model is loaded in LM Studio
- ✅ Test the endpoint: `curl http://localhost:1234/v1/models`

### Pinecone Errors
- ✅ Verify your API key is correct
- ✅ Check your Pinecone dashboard for quota limits
- ✅ Ensure the index name doesn't contain invalid characters

### Port Already in Use
- Change `FLASK_PORT` in `.env` to a different port (e.g., 5001)

### Module Not Found Errors
- Ensure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Web Browser   │────▶│  Flask Server   │────▶│   LM Studio     │
│   (Chat UI)     │     │   (app.py)      │     │   (Local LLM)   │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │                 │
                        │    Pinecone     │
                        │  (Vector DB)    │
                        │                 │
                        └─────────────────┘
```

---

## 📝 Tech Stack

- **Backend**: Python, Flask, Flask-CORS
- **LLM Client**: OpenAI Python SDK (compatible with LM Studio)
- **Vector Database**: Pinecone
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LM Studio](https://lmstudio.ai/) - Local LLM inference
- [Pinecone](https://www.pinecone.io/) - Vector database
- [Sentence-Transformers](https://www.sbert.net/) - Text embeddings
- [Flask](https://flask.palletsprojects.com/) - Web framework

---

**Built with ❤️ for the Diligent "Code Meets Co-Pilot" Workshop**
