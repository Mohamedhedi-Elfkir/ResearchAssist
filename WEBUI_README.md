# Research Agent - NotebookLM-like Web UI

A modern web interface for the Research Agent with real-time streaming responses, document management, and conversation history.

## ✨ Features

- **Document Management**: Upload PDF, TXT, and MD files with drag-and-drop
- **Real-time Streaming**: See AI responses as they're generated
- **Conversation History**: Manage multiple research sessions
- **Source Citations**: View and explore document sources used in answers
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m backend.main
```

The API will run at: http://localhost:8000

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The UI will run at: http://localhost:5173

### 3. Open Your Browser

Navigate to http://localhost:5173 and start researching!

## 📁 Project Structure

```
Agent/
├── backend/              # FastAPI backend
│   ├── api/             # API routes and schemas
│   ├── services/        # Business logic
│   ├── database/        # SQLAlchemy models and CRUD
│   └── middleware/      # CORS and error handling
├── frontend/            # React frontend
│   └── src/
│       ├── components/  # UI components
│       ├── hooks/       # Custom React hooks
│       ├── stores/      # Zustand state management
│       ├── lib/         # API client and utilities
│       └── types/       # TypeScript types
├── src/                 # Original agent code (unchanged)
└── main.py             # Original CLI (unchanged)
```

## 🎯 Usage

### Upload Documents

1. Click on the "Documents" tab in the left sidebar
2. Drag and drop files or click to browse
3. Wait for documents to be ingested

### Start a Conversation

1. Click "New Chat" in the left sidebar
2. Type your research question
3. Watch as the AI streams its response
4. Click on sources to see which documents were used

### Manage Sessions

- Create multiple conversations for different topics
- Each session maintains its own message history
- Archive or delete sessions as needed

## 🔧 Configuration

### Backend (.env)

Located in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_FILE_SIZE_MB=50
RETRIEVAL_TOP_K=5
RELEVANCE_THRESHOLD=7.0
GEMINI_MODEL=gemini-1.5-flash-latest
```

### Frontend (.env)

Located in `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 🌐 API Endpoints

### Documents
- `POST /api/v1/documents/upload` - Upload a document
- `GET /api/v1/documents` - List all documents
- `DELETE /api/v1/documents/{id}` - Delete a document

### Sessions
- `POST /api/v1/chat/sessions` - Create a new session
- `GET /api/v1/chat/sessions` - List all sessions
- `GET /api/v1/chat/sessions/{id}` - Get session details
- `DELETE /api/v1/chat/sessions/{id}` - Delete a session

### Chat
- `GET /api/v1/chat/sessions/{id}/stream` - Stream research responses (SSE)

### Health
- `GET /api/v1/health` - Check API status

## 🔄 Server-Sent Events (SSE)

The streaming endpoint emits these events:

- `node_start` - Workflow node begins execution
- `node_complete` - Workflow node finishes
- `token` - Individual token from the LLM
- `synthesis_complete` - Final answer with sources and metadata
- `complete` - Message saved to database
- `error` - Error occurred during processing

## 📊 Database

SQLite database at `data/research_agent.db` with tables:

- `sessions` - Chat conversations
- `messages` - Individual messages
- `documents` - Uploaded file metadata
- `session_documents` - Links between sessions and documents

## 🎨 Tech Stack

### Backend
- FastAPI - Modern, fast Python web framework
- SQLAlchemy - SQL ORM
- SSE-Starlette - Server-Sent Events support
- Existing LangChain/LangGraph workflow (unchanged)

### Frontend
- React 18 + TypeScript
- Vite - Fast build tool
- Tailwind CSS - Utility-first CSS
- Zustand - State management
- Axios - HTTP client
- React Markdown - Markdown rendering
- Lucide React - Icon library

## 🔍 Troubleshooting

### Backend won't start
- Check that `GEMINI_API_KEY` is set in `.env`
- Ensure port 8000 is not in use
- Verify Python dependencies are installed

### Frontend won't start
- Check that `node_modules` is installed (`npm install`)
- Ensure port 5173 is not in use
- Verify `.env` file exists in `frontend/` directory

### Streaming not working
- Check browser console for errors
- Verify backend is running and accessible
- Ensure CORS is properly configured

### Documents not uploading
- Check file size (max 50MB)
- Verify file type (PDF, TXT, MD only)
- Check backend logs for errors

## 🚢 Production Deployment

### Backend
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
# Build for production
cd frontend
npm run build

# Serve with nginx or any static file server
# Built files will be in frontend/dist/
```

## 📝 Notes

- The original CLI (`python main.py`) still works
- Vector store (Chroma) is shared between CLI and web UI
- All existing agent functionality is preserved
- No changes to core agent code in `src/` directory

## 🤝 Contributing

This is built on top of the original Research Agent. Any improvements to the core agent automatically benefit the web UI.

## 📄 License

MIT License

---

**Built with ❤️ using Claude Code**
