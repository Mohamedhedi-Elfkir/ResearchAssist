# Research Agent with LangGraph and RAG

A powerful research agent built with LangChain, LangGraph, and RAG (Retrieval-Augmented Generation) that can search through local documents and web content to answer research questions.

## Features

- **RAG-based Document Search**: Search through local PDF, TXT, and Markdown files
- **Web Scraping**: Extract information from web pages
- **LangGraph Workflow**: Intelligent multi-step research process
- **Vector Database**: Chroma for efficient document storage and retrieval
- **Google Gemini Integration**: Powered by Google's Gemini LLM
- **CLI Interface**: Easy-to-use command-line interface
- **Modular Architecture**: Clean, maintainable code structure

## Architecture

```
START
  ↓
Query Analysis (determine rag/web/both)
  ↓
Research Planning (break into sub-questions)
  ↓
  ├─→ RAG Retrieval ──┐
  ├─→ Web Scraping ───┤
  └─→ Both ───────────┘
        ↓
  Relevance Check
        ↓
  ┌─────┴─────┐
  │           │
Sufficient  Insufficient
  │           │
  │     Re-query/Web Search
  │           │
  └─────┬─────┘
        ↓
   Synthesis
        ↓
      END
```

## Installation

### 1. Clone or download this repository

```bash
cd Agent
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and add your Google Gemini API key:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
GEMINI_API_KEY=your_api_key_here
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

## Quick Start

### 1. Download Large Documents (Optional)

Download documents directly from URLs and automatically ingest them:

```bash
# Download a single document
python main.py download --url https://arxiv.org/pdf/1706.03762.pdf --auto-ingest

# Download multiple documents
python main.py download --url https://arxiv.org/pdf/1706.03762.pdf https://arxiv.org/pdf/2005.14165.pdf --auto-ingest

# Download with custom filename
python main.py download --url https://example.com/paper.pdf --filename research_paper.pdf
```

**Popular sources for large documents:**
- Research Papers: [ArXiv](https://arxiv.org) - `https://arxiv.org/pdf/[paper-id].pdf`
- Books: [Project Gutenberg](https://www.gutenberg.org) - Public domain books
- Documentation: Python, Django, TensorFlow docs (PDF format)
- Wikipedia: Use the Wikipedia PDF API

### 2. Ingest Local Documents

Add your documents to the `data/documents/` folder, then run:

```bash
python main.py ingest --path data/documents
```

Supported file types: PDF, TXT, MD (Markdown)

### 3. Query the Agent

```bash
python main.py query "What is machine learning?"
```

### 4. Interactive Mode

```bash
python main.py interactive
```

## Usage Examples

### Command Line

#### Ingest multiple directories

```bash
python main.py ingest --path data/documents data/papers data/notes
```

#### Research query

```bash
python main.py query "Explain neural networks in simple terms"
```

### Programmatic Usage

```python
from main import ResearchAgent

# Initialize agent
agent = ResearchAgent()

# Ingest documents
agent.ingest_documents(["data/documents"])

# Research a query
result = agent.research("What is deep learning?")

print(result["answer"])
print(result["sources"])
```

### Run Examples

```bash
# Basic research example
python examples/basic_research.py

# Web scraping example
python examples/web_research.py
```

## Project Structure

```
Agent/
├── src/
│   ├── config.py              # Configuration management
│   ├── graph/
│   │   ├── state.py           # LangGraph state
│   │   ├── nodes.py           # Workflow nodes
│   │   └── workflow.py        # Workflow construction
│   ├── rag/
│   │   ├── vector_store.py    # Chroma vector store
│   │   ├── embeddings.py      # Embedding generation
│   │   ├── retriever.py       # Document retrieval
│   │   └── chunking.py        # Text chunking
│   ├── loaders/
│   │   ├── file_loader.py     # Document loaders
│   │   ├── web_scraper.py     # Web scraping
│   │   └── document_processor.py  # Processing
│   ├── llm/
│   │   ├── gemini_client.py   # Gemini API client
│   │   └── prompts.py         # Prompt templates
│   └── utils/
│       └── logger.py          # Logging
├── data/
│   ├── documents/             # Local documents
│   └── chroma_db/             # Vector database
├── examples/
│   ├── basic_research.py      # Basic example
│   └── web_research.py        # Web example
├── main.py                    # CLI entry point
├── requirements.txt
└── README.md
```

## Configuration

All configuration is managed through environment variables in `.env`:

```bash
# Google Gemini API
GEMINI_API_KEY=your_api_key_here

# Vector Store
CHROMA_PERSIST_DIRECTORY=./data/chroma_db

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_FILE_SIZE_MB=50

# Agent Configuration
MAX_ITERATIONS=3
RETRIEVAL_TOP_K=5
RELEVANCE_THRESHOLD=7.0

# LLM Configuration
GEMINI_MODEL=gemini-1.5-pro
TEMPERATURE=0.7
MAX_TOKENS=8192

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/agent.log
```

## How It Works

### 1. Document Ingestion

- Documents are loaded from local files (PDF, TXT, MD)
- Text is extracted and preprocessed
- Documents are split into chunks (1000 chars with 200 char overlap)
- Embeddings are generated using Google's text-embedding-004
- Chunks are stored in Chroma vector database

### 2. Query Processing

- User submits a research query
- **Query Analysis**: Determines if local search, web search, or both are needed
- **Research Planning**: Breaks complex queries into sub-questions
- **Retrieval**: Searches vector store for relevant documents
- **Relevance Check**: LLM evaluates if retrieved documents are sufficient
- **Synthesis**: LLM generates comprehensive answer with citations

### 3. LangGraph Workflow

The agent uses LangGraph to orchestrate a multi-step research process:
- Conditional routing based on query analysis
- Iterative refinement if initial results are insufficient
- Automatic fallback to web search if local knowledge is incomplete

## Advanced Usage

### Custom Vector Store

```python
from src.rag.vector_store import create_vector_store

# Create a custom collection
vector_store = create_vector_store(
    collection_name="my_research",
    persist_directory="./custom_db"
)
```

### Web Scraping

```python
from src.loaders.web_scraper import WebScraper

scraper = WebScraper()
documents = scraper.scrape_urls([
    "https://example.com/article1",
    "https://example.com/article2"
])
```

### Custom Workflow

```python
from src.graph.workflow import ResearchWorkflow
from src.rag.vector_store import create_vector_store

vector_store = create_vector_store()
workflow = ResearchWorkflow(vector_store)

result = workflow.run("Your research question")
```

## Troubleshooting

### API Key Error

If you see "GEMINI_API_KEY is required":
- Make sure you've created a `.env` file
- Add your API key: `GEMINI_API_KEY=your_key_here`
- Restart the agent

### No Documents Found

If the agent can't find documents:
- Check that files are in `data/documents/` folder
- Ensure file formats are supported (PDF, TXT, MD)
- Try running ingest command again

### Import Errors

If you see import errors:
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

## Limitations

- **Web Search**: Currently requires manual URL input. Integrate with Google Custom Search API or similar for automatic web search
- **File Types**: Limited to PDF, TXT, and MD. Can be extended to support DOCX, HTML, etc.
- **Multimodal**: Text-only. Can be enhanced to support images, tables, etc.

## Future Enhancements

- [ ] Integration with Google Custom Search API
- [ ] Support for more file types (DOCX, HTML, CSV)
- [ ] Multi-modal support (images, tables)
- [ ] Conversation history and context
- [ ] Streaming responses
- [ ] API server mode
- [ ] Web UI

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License

## Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Powered by [Google Gemini](https://ai.google.dev/)
- Vector database by [Chroma](https://www.trychroma.com/)
