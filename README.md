# AI Agent with Multiple Tools

[![Tests](https://github.com/paulmattei/ai-agent-starter/actions/workflows/test.yml/badge.svg)](https://github.com/paulmattei/ai-agent-starter/actions/workflows/test.yml)
[![Deploy](https://github.com/paulmattei/ai-agent-starter/actions/workflows/deploy.yml/badge.svg)](https://github.com/paulmattei/ai-agent-starter/actions/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/paulmattei/ai-agent-starter/branch/main/graph/badge.svg)](https://codecov.io/gh/paulmattei/ai-agent-starter)
![Python](https://img.shields.io/badge/python-3.11+-blue)

A clean, production-ready AI agent template built with [aisuite](https://github.com/andrewyng/aisuite), featuring secure code execution ([E2B](https://e2b.dev)), web search ([Tavily](https://tavily.com)), and automated deployment to [Fly.io](https://fly.io) via GitHub Actions.

## Features

- 🤖 **Unified AI Interface**: Use aisuite to work with multiple LLM providers (OpenAI, Anthropic, Google, etc.)
- 💻 **Code Execution**: Safe Python code execution in E2B sandboxes
- 🔍 **Web Search**: Real-time information retrieval via Tavily
- 📊 **Production Logging**: Standard Python logging with timestamps for debugging and monitoring
- 🧪 **Full Testing**: Unit tests + E2E tests with complete tracing
- 🏗️ **Modular Architecture**: Tools organized in `tools/` directory for easy extension
- 🚀 **Production Ready**: Containerized and deployed on Fly.io
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

## Getting Started

### Prerequisites

You'll need API keys for:
- **OpenAI**: https://platform.openai.com/api-keys (or another LLM provider)
- **E2B**: https://e2b.dev (for code execution)
- **Tavily**: https://tavily.com (for web search)

### Installation

```bash
# Clone and install
git clone git@github.com:paulmattei/ai-agent-starter.git
cd ai-agent-starter
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env and add your API keys:
# OPENAI_API_KEY=sk-...
# E2B_API_KEY=e2b_...
# TAVILY_API_KEY=tvly-...

# Run locally
python main.py
```

The server will start at `http://localhost:8080`

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tools --cov=utils --cov=main --cov-report=term
```

**CI/CD:** Automated testing on every push; auto-deploy to Fly.io on merge to main

See **[TESTING.md](TESTING.md)** for detailed testing documentation.

### Try It Out

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

## Deployment

This project auto-deploys to Fly.io via GitHub Actions on every push to `main`.

### Setup (One-time)

```bash
# Install Fly CLI
brew install flyctl  # macOS
# OR: curl -L https://fly.io/install.sh | sh  # Linux

# Create app
flyctl auth login
flyctl apps create ai-agent-starter

# Set secrets (easy way)
./scripts/set-fly-secrets.sh

# Create deploy token and add to GitHub Secrets as FLY_API_TOKEN
fly tokens create deploy --name "github-actions-cd" --expiry 2160h --app ai-agent-starter
```

See **[CI/CD Setup Guide](.github/CICD_SETUP.md)** for detailed deployment instructions.

### Manual Deploy

```bash
flyctl deploy
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
│   └── logging.py          # Standard Python logging
├── scripts/                 # Deployment scripts
│   ├── README.md           # Scripts documentation
│   └── set-fly-secrets.sh  # Auto-set Fly.io secrets from .env
├── test_tools.py           # Unit tests (9 tests)
├── test_agent.py           # E2E tests with tracing (5 tests)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container configuration
├── fly.toml                # Fly.io deployment config
├── env.example             # Example environment variables
├── ARCHITECTURE.md         # Detailed architecture docs
├── TESTING.md              # Comprehensive testing guide
└── README.md               # This file
```

## Configuration

### Agent Behavior

The agent uses a system message for intelligent tool selection. Edit the `system_message` in `main.py` to customize behavior. Key settings:
- **Max iterations**: `max_turns=3` (up to 3 tool calling rounds)
- **Multi-tool orchestration**: Can combine tools for complex tasks
- **Tool guidelines**: Math/code → `execute_code`, current events → `search_web`

### Logging

Production-ready logging with timestamps, request tracing, and tool execution tracking:

```
2025-10-18 14:56:06 [INFO] 📩 NEW CHAT REQUEST
2025-10-18 14:56:06 [INFO] Model: openai:gpt-4o
2025-10-18 14:56:07 [INFO] 🔧 Executing code in E2B sandbox...
2025-10-18 14:56:08 [INFO] ✅ CHAT REQUEST COMPLETED (total: 2.15s)
```

## Extending the Agent

### Add a New Tool

1. Create `tools/your_tool.py` with your function
2. Register it in `tools/__init__.py`:
   ```python
   from .your_tool import your_tool
   AVAILABLE_TOOLS = [execute_code, search_web, your_tool]
   ```

### Switch LLM Provider

Change the model parameter in requests:
```bash
# Anthropic
{"message": "Hello", "model": "anthropic:claude-3-5-sonnet-20241022"}

# Google
{"message": "Hello", "model": "google:gemini-1.5-pro"}
```

## Documentation & Resources

- 📖 **[Architecture Guide](ARCHITECTURE.md)** - System design and tool specifications
- 🧪 **[Testing Guide](TESTING.md)** - Testing documentation and coverage matrices
- 🚀 **[CI/CD Setup](.github/CICD_SETUP.md)** - Deployment configuration
- 📝 **[Changelog](CHANGELOG.md)** - Recent updates

**External Docs:**
- [aisuite](https://github.com/andrewyng/aisuite) | [E2B](https://e2b.dev/docs) | [Fly.io](https://fly.io/docs) | [Tavily](https://docs.tavily.com)

## License

MIT License - feel free to use this as a foundation for your own projects!

