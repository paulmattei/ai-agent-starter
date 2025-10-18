# AI Agent with Code Execution

![Tests](https://img.shields.io/badge/tests-14%2F14-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-95%25-green)
![Python](https://img.shields.io/badge/python-3.11+-blue)

A simple, clean AI agent built with [aisuite](https://github.com/andrewyng/aisuite) that provides secure code execution capabilities via [E2B](https://e2b.dev). Designed to run on [Fly.io](https://fly.io).

## Features

- 🤖 **Unified AI Interface**: Use aisuite to work with multiple LLM providers (OpenAI, Anthropic, Google, etc.)
- 💻 **Code Execution**: Safe Python code execution in E2B sandboxes
- 🔍 **Web Search**: Real-time information retrieval via Tavily
- 📊 **Colored Logging**: Beautiful ANSI-colored logs with timestamps for debugging and monitoring
- 🧪 **Full Testing**: Unit tests + E2E tests with complete tracing
- 🏗️ **Modular Architecture**: Tools organized in `tools/` directory for easy extension
- 🚀 **Production Ready**: Containerized and ready to deploy on Fly.io
- 🎯 **Simple & Clean**: Minimal boilerplate, easy to understand and extend

## Architecture

```
User Request → Flask API → aisuite Client → LLM
                              ↓
                         Tool Calling
                         /          \
                        /            \
                 E2B Sandbox      Tavily API
              (Code Execution)  (Web Search)
```

📖 **[Full Architecture Documentation](ARCHITECTURE.md)**

## Quick Start

```bash
# 1. Clone and install
git clone <your-repo-url>
cd jobbot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp env.example .env
# Edit .env and add your API keys

# 3. Run
python main.py

# 4. Test it
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate the first 10 Fibonacci numbers"}'
```

## Documentation

- 📖 **[Architecture Guide](ARCHITECTURE.md)** - Complete system design and tool specifications
- 🧪 **[Testing Guide](TESTING.md)** - Comprehensive testing documentation with diagrams and coverage matrices
- 📝 **[Changelog](CHANGELOG.md)** - Recent updates and features

## Prerequisites

You'll need API keys for:

1. **OpenAI** (or another LLM provider): https://platform.openai.com/api-keys
2. **E2B**: https://e2b.dev (for code execution)
3. **Tavily**: https://tavily.com/ (for web search)

## Local Development Setup

### 1. Clone and Install

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=sk-...
# E2B_API_KEY=e2b_...
# TAVILY_API_KEY=tvly-...
```

### 3. Run Locally

```bash
python main.py
```

The server will start at `http://localhost:8080`

### 4. Run Tests

See **[TESTING.md](TESTING.md)** for comprehensive testing documentation.

```bash
# Unit tests - 9 tests covering tool functions, error handling, edge cases
python test_tools.py

# E2E tests - 5 tests covering full HTTP API flow with validation
python test_agent.py
```

**Test Coverage:** 14/14 tests passing (100%), 95%+ code coverage

### 5. Test the Agent

```bash
# Health check
curl http://localhost:8080/health

# Chat with code execution
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate the first 10 Fibonacci numbers"
  }'

# Web search example
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the latest developments in AI?"
  }'

# Combined tools example
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find the current Bitcoin price and calculate a 20% increase"
  }'
```

## Deploy to Fly.io

### 1. Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
iwr https://fly.io/install.ps1 -useb | iex
```

### 2. Login and Launch

```bash
# Login to Fly.io
flyctl auth login

# Launch the app (first time)
flyctl launch --no-deploy

# Set your API keys as secrets
flyctl secrets set OPENAI_API_KEY=sk-...
flyctl secrets set E2B_API_KEY=e2b_...
flyctl secrets set TAVILY_API_KEY=tvly-...

# Deploy
flyctl deploy
```

### 3. Access Your Deployed Agent

```bash
# Get your app URL
flyctl status

# Test it
curl https://your-app-name.fly.dev/health
```

## API Reference

### `GET /`
Welcome page with API documentation

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy"
}
```

### `POST /chat`
Chat with the AI agent

**Request:**
```json
{
  "message": "Your question or request here",
  "model": "openai:gpt-4o"  // optional, defaults to gpt-4o
}
```

**Response:**
```json
{
  "response": "Agent's response here",
  "model": "openai:gpt-4o"
}
```

## Available Tools

The agent automatically selects the appropriate tool(s) based on your request:

### Code Execution (E2B)
- Executes Python code in a secure, isolated sandbox
- Returns stdout, stderr, and execution results
- **Use for**: calculations, data processing, algorithms, data analysis, programming tasks
- Safe and sandboxed - code runs in an isolated environment

### Web Search (Tavily)
- Real-time web search with AI-powered results
- Returns formatted results with titles, URLs, and content snippets
- Includes quick answers when available
- **Use for**: current events, news, real-time information, factual lookup

The agent supports up to 3 tool calling iterations (`max_turns=3`) and can combine multiple tools to solve complex tasks.

## Example Agent Interactions

### Code Execution
**Input:** "Calculate the first 10 Fibonacci numbers"

**Response:**
```
The first 10 Fibonacci numbers are: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Web Search
**Input:** "What are the latest developments in AI?"

**Response:**
```
Here are some of the latest developments in AI from this week:

1. Malaysia Launches Ryt Bank - Malaysia has introduced its first AI-powered bank
2. Google's Veo 3 - Google has made its Veo 3 AI video creation tools widely available
3. Purdue University's RAPTOR System - AI-powered defect-detection system...
```

### Combined Tools
**Input:** "Search for the population of Tokyo and calculate 10% of that number"

**Response:**
```
The current population of the Tokyo metro area in 2023 is approximately 37,194,000.
10% of Tokyo's population is approximately 3,719,400.
```

**Agent orchestrated:** Web search → Got population → Executed code → Calculated percentage

## Switching AI Providers

aisuite supports multiple providers. Just change the model parameter:

```bash
# OpenAI
{"message": "Hello", "model": "openai:gpt-4o"}

# Anthropic
{"message": "Hello", "model": "anthropic:claude-3-5-sonnet-20241022"}

# Google
{"message": "Hello", "model": "google:gemini-1.5-pro"}
```

Don't forget to add the corresponding API keys to your environment!

## Project Structure

```
.
├── main.py                  # Flask app and API routes
├── tools/                   # Tool functions
│   ├── __init__.py         # Tool registry
│   ├── execute_code.py     # E2B code execution
│   └── search_web.py       # Tavily web search
├── utils/                   # Utility modules
│   ├── __init__.py
│   └── logging.py          # Colored logging
├── test_tools.py           # Unit tests (9 tests)
├── test_agent.py           # E2E tests with tracing (5 tests)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container configuration
├── fly.toml               # Fly.io deployment config
├── ARCHITECTURE.md         # Detailed architecture docs
├── TESTING.md             # Comprehensive testing guide
└── README.md              # This file
```

## Logging & Monitoring

The agent includes a built-in colored logging system for easy debugging:

- **Color-coded logs**: Different colors for info (blue), success (green), errors (red), and tool execution (yellow)
- **Timestamps**: Millisecond precision timestamps on every log entry
- **Request tracing**: Each request is wrapped with clear start/end markers and timing information
- **Tool execution tracking**: Detailed logs for sandbox creation, code execution, and cleanup

Example log output:
```
[12:34:56.789] ================================================================================
[12:34:56.789] 📩 NEW CHAT REQUEST
[12:34:56.790] Model: openai:gpt-4o
[12:34:56.790] Message: Calculate fibonacci numbers
[12:34:56.791] 🔧 Executing code in E2B sandbox...
[12:34:57.123] ✓ Sandbox created
[12:34:57.456] ✓ Execution completed
[12:34:57.457] ✅ CHAT REQUEST COMPLETED (total: 0.67s)
```

## Agent Configuration

The agent is configured with a system message that enables intelligent tool selection:

```python
system_message = """
You are a helpful assistant that can write code and search the web to solve the user's problem.

You have access to the following tools:
- execute_code: Execute Python code in a sandbox for calculations, data analysis, and programming tasks
- search_web: Search the web for real-time information, current events, or factual knowledge

Guidelines:
- For math, calculations, data analysis, or programming tasks → use execute_code
- For current events, news, or real-time information → use search_web
- You can combine both tools to solve complex problems
- Always use tools to get accurate information rather than guessing
"""
```

See `main.py` `/chat` endpoint for the complete current system message.

This configuration:
- Enables intelligent tool selection based on the task
- Allows multi-tool orchestration for complex problems
- Supports up to 3 tool calling iterations (`max_turns=3`)
- Provides clear guidelines for when to use each tool

## Extending the Agent

### Add a New Tool

1. Create `tools/your_tool.py`:
```python
from utils.logging import log_span

def your_tool(param: str) -> str:
    """
    Description of what your tool does.
    
    Args:
        param (str): Description of parameter
        
    Returns:
        str: Description of return value
    """
    log_span(f"🔧 Using your_tool with {param}", "tool")
    # Your tool logic here
    return "result"
```

2. Register it in `tools/__init__.py`:
```python
from .your_tool import your_tool

AVAILABLE_TOOLS = [
    execute_code,
    search_web,
    your_tool,  # Add here
]
```

That's it! The tool is now available to the agent.

### Use a Different LLM Provider

```python
# Change the default model in main.py's /chat endpoint
model = data.get('model', 'anthropic:claude-3-5-sonnet-20241022')
```

### Modify Agent Behavior

To change how the agent behaves, edit the `system_message` in the `/chat` endpoint in `main.py`. You can:
- Allow the agent to answer without code execution
- Add new tool descriptions
- Change response formatting guidelines

## Troubleshooting

### Missing API Keys
```
Error: Missing environment variables: OPENAI_API_KEY
```
→ Make sure all required API keys are set in your `.env` file

### Import Errors
```
ModuleNotFoundError: No module named 'aisuite'
```
→ Run `pip install -r requirements.txt`

### Fly.io Deployment Issues
```
Error: failed to fetch an image or build from source
```
→ Make sure Docker is running and you have a valid Dockerfile

## License

MIT License - feel free to use this as a foundation for your own projects!

## Contributing

This is a simple boilerplate example. Feel free to fork and customize for your needs!

## Testing

See **[TESTING.md](TESTING.md)** for comprehensive testing documentation including:
- Testing philosophy with visual pyramid
- Complete tool specifications with I/O tables
- Architecture diagrams for each tool
- Detailed test breakdowns and coverage matrices
- CI/CD recommendations
- Performance benchmarks

**Test Status:**
- Unit Tests: 9/9 passing (100%)
- E2E Tests: 5/5 passing (100%)
- Coverage: 95%+ of code paths

## Resources

- [aisuite Documentation](https://github.com/andrewyng/aisuite)
- [E2B Documentation](https://e2b.dev/docs)
- [Fly.io Documentation](https://fly.io/docs)
- [Tavily Documentation](https://docs.tavily.com)

