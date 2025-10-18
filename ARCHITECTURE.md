# Jobbot Architecture

## Overview
Jobbot is a Flask-based AI agent with tool calling capabilities using aisuite and E2B code execution sandboxes.

## Project Structure

```
jobbot/
├── main.py              # Flask application and API routes
├── tools/               # Tool functions for AI agent
│   ├── __init__.py     # Tool registry and exports
│   └── execute_code.py # E2B code execution tool
├── utils/              # Utility modules
│   ├── __init__.py     # Utils exports
│   └── logging.py      # Colored logging utilities
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not in git)
├── env.example         # Example environment variables
└── Dockerfile          # Container configuration
```

## Module Descriptions

### `main.py`
The main Flask application that provides:
- `/health` - Health check endpoint
- `/chat` - Main chat endpoint for AI agent interaction
- `/` - API documentation endpoint

### `tools/`
Contains all tool functions that the AI agent can use:

**`execute_code.py`**
- Provides safe Python code execution in E2B sandboxes
- Handles sandbox lifecycle (create, execute, cleanup)
- Returns formatted execution results
- Use for: math, calculations, data analysis, programming tasks

**`search_web.py`**
- Web search using Tavily API
- Returns formatted search results with titles, URLs, and content
- Includes quick answers when available
- Use for: current events, real-time information, factual knowledge

**`__init__.py`**
- Exports all available tools
- Maintains `AVAILABLE_TOOLS` registry for easy tool management

### `utils/`
Shared utility functions:

**`logging.py`**
- Colored terminal output with ANSI codes
- Timestamped log spans for tracing
- Log levels: info, success, error, tool

## Adding New Tools

To add a new tool (for capabilities beyond code execution):

1. Create a new file in `tools/` (e.g., `tools/search_web.py`)
2. Implement your tool function with clear docstring
3. Import and add to `AVAILABLE_TOOLS` in `tools/__init__.py`

Example for a web search tool:
```python
# tools/search_web.py
from utils.logging import log_span

def search_web(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query (str): Search query
        
    Returns:
        str: Search results
    """
    log_span(f"🔍 Searching web for: {query}", "tool")
    # Implementation here
    return results
```

```python
# tools/__init__.py
from .execute_code import execute_code
from .search_web import search_web

AVAILABLE_TOOLS = [
    execute_code,
    search_web,  # Add new tool here
]

```

**Note**: The `execute_code` tool is the primary tool - the LLM converts natural language requests (including math, data analysis, etc.) into Python code that runs in E2B. Only add new tools for capabilities that can't be achieved through code execution.

## Environment Variables

Required environment variables:
- `OPENAI_API_KEY` - OpenAI API key for aisuite
- `E2B_API_KEY` - E2B API key for code execution  
- `TAVILY_API_KEY` - Tavily API key for web search
- `PORT` - Server port (default: 8080)

Get API keys:
- OpenAI: https://platform.openai.com/api-keys
- E2B: https://e2b.dev/docs
- Tavily: https://tavily.com/

## Design Principles

1. **Modularity**: Tools are isolated in their own files
2. **Single Responsibility**: Each module has one clear purpose
3. **Easy Extension**: Adding new tools requires minimal changes
4. **Clean Imports**: All tools imported from one registry
5. **Good Logging**: Colored, timestamped logs for debugging
6. **Type Hints**: Functions use type annotations for clarity

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp env.example .env
# Edit .env with your API keys

# Run the server
python main.py
```

## Testing

### Unit Tests (`test_tools.py`)
Tests individual tool functions in isolation:
```bash
python test_tools.py
```

Validates:
- ✅ Module imports work correctly
- ✅ Logging utilities function
- ✅ Tool registry is properly configured
- ✅ Each tool executes successfully

### End-to-End Tests (`test_agent.py`)
Tests the full Flask API via HTTP requests with response validation:
```bash
python test_agent.py
```

**What it does:**
- Starts Flask server in background thread
- Makes HTTP POST requests to `/chat` endpoint
- Validates response correctness, not just existence

**Test scenarios:**
1. **Health Endpoint**: `/health` returns 200
2. **Code Execution**: Fibonacci numbers - validates correct sequence in response
3. **Web Search**: Capital of France - validates "Paris" is mentioned
4. **Combined Tools**: Tokyo population + calculation - validates both search and code results
5. **Complex Code**: Prime numbers + sum - validates correct primes and sum (28)

Example output with validation:
```
📩 HTTP REQUEST to /chat
Message: Calculate the first 10 Fibonacci numbers
✅ HTTP 200 OK (took 5.2s)
Response: The first 10 Fibonacci numbers are: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
✅ Response contains correct Fibonacci numbers
```

### Manual Testing

Test individual tools directly:
```python
from tools.execute_code import execute_code
from tools.search_web import search_web

# Test code execution
result = execute_code("print('Hello, World!')")
print(result)

# Test web search
result = search_web("latest Python news")
print(result)
```

