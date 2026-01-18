# Web UI Setup Guide

## Backend Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
python -m backend.main
```

The API will be available at: http://localhost:8000

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/v1/health

### 3. Test the API

**Health Check:**
```bash
curl http://localhost:8000/api/v1/health
```

**Create a Session:**
```bash
curl -X POST http://localhost:8000/api/v1/chat/sessions \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Research Session"}'
```

**Upload a Document:**
```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@path/to/your/document.pdf"
```

**Stream a Query (in browser console):**
```javascript
const eventSource = new EventSource('http://localhost:8000/api/v1/chat/sessions/1/stream?query=What%20is%20AI');

eventSource.addEventListener('node_start', (e) => {
  console.log('Node started:', JSON.parse(e.data));
});

eventSource.addEventListener('synthesis_complete', (e) => {
  console.log('Answer ready:', JSON.parse(e.data));
});

eventSource.addEventListener('complete', (e) => {
  console.log('Done:', JSON.parse(e.data));
  eventSource.close();
});

eventSource.addEventListener('error', (e) => {
  console.error('Error:', e.data);
});
```

## API Endpoints

### Health
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed system status

### Documents
- `POST /api/v1/documents/upload` - Upload a document
- `GET /api/v1/documents` - List all documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete a document
- `GET /api/v1/documents/stats` - Get statistics

### Sessions
- `POST /api/v1/chat/sessions` - Create a new session
- `GET /api/v1/chat/sessions` - List all sessions
- `GET /api/v1/chat/sessions/{id}` - Get session with messages
- `PATCH /api/v1/chat/sessions/{id}` - Update session
- `DELETE /api/v1/chat/sessions/{id}` - Delete session

### Chat
- `POST /api/v1/chat/sessions/{id}/messages` - Send message (non-streaming)
- `GET /api/v1/chat/sessions/{id}/stream?query=...` - Stream research (SSE)

## Database

The SQLite database is automatically created at `data/research_agent.db` on first run.

### Tables:
- `sessions` - Chat sessions
- `messages` - Chat messages
- `documents` - Uploaded documents metadata
- `session_documents` - Links between sessions and documents

## SSE Events

The streaming endpoint emits these events:

- `node_start` - Workflow node begins
- `node_complete` - Workflow node completes
- `token` - Individual LLM token (if available)
- `synthesis_complete` - Final answer with sources
- `complete` - Message saved, includes message_id
- `error` - Error occurred

## Frontend (Coming Next)

The React frontend will be initialized next. It will connect to this backend API.

## Notes

- Make sure your `.env` file has `GEMINI_API_KEY` configured
- The vector store (Chroma) is shared with the CLI version
- All existing CLI functionality remains available
