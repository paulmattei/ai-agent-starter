# Changelog

## 2025-10-18 - Continuous Deployment Added

### New Features
- ✅ Automatic deployment to Fly.io via GitHub Actions
- ✅ CD pipeline runs after successful tests on main branch
- ✅ Deployment badge added to README
- ✅ **Security**: Uses scoped deploy tokens following Fly.io best practices

### Files Added
```
.github/workflows/
  ├── test.yml            # CI: Run tests on push/PR
  └── deploy.yml          # NEW: CD: Deploy to Fly.io on main
.github/
  ├── CICD_SETUP.md       # Complete CI/CD setup guide
  ├── CD_QUICKSTART.md    # Quick 5-minute setup
  └── workflows/README.md # Workflow documentation
scripts/
  ├── README.md           # Scripts documentation
  └── set-fly-secrets.sh  # NEW: Auto-set Fly.io secrets from .env
```

### Setup Requirements (Updated for Security)
To enable CD, create a **scoped deploy token** and add to GitHub Secrets:

```bash
# Create app-scoped token (90 days, custom name)
fly tokens create deploy \
  --name "github-actions-cd" \
  --expiry 2160h \
  --app ai-agent-starter
```

Then add as `FLY_API_TOKEN` in GitHub Settings → Secrets → Actions

**Important Changes:**
- ❌ **DON'T** use `fly auth token` (deprecated, all-powerful, short-lived)
- ✅ **DO** use `fly tokens create deploy` (scoped, named, with expiry)
- ✅ Set expiry times (90 days recommended)
- ✅ Rotate tokens regularly

See [Fly.io Token Best Practices](https://fly.io/docs/security/tokens/)

### Deployment Flow
```
Push to main → Run tests (CI) → Tests pass → Deploy to Fly.io (CD)
                              ↘ Tests fail → No deployment
```

### Benefits
- **Zero-touch deployment**: Merge to main = automatic production deployment
- **Safety**: Only deploys if all tests pass
- **Speed**: No manual steps required
- **Reliability**: Consistent deployment process every time

---

## 2025-10-18 - Web Search Tool Added

### New Features
- ✅ Added Tavily-powered web search tool
- ✅ Modular architecture with `tools/` and `utils/` directories
- ✅ Comprehensive test suite

### Files Added
```
tools/
  ├── execute_code.py    # E2B code execution
  ├── search_web.py      # NEW: Tavily web search
  └── __init__.py        # Tool registry

utils/
  ├── logging.py         # Colored logging utilities
  └── __init__.py        # Utils exports

tests/
  ├── test_tools.py      # Unit tests for all tools
  └── test_agent.py      # E2E tests
ARCHITECTURE.md          # Complete architecture documentation
```

### Dependencies Added
- `tavily-python>=0.3.0` - Web search API

### Environment Variables
Added required variable:
- `TAVILY_API_KEY` - Get from https://tavily.com/

### System Prompt Updated
Agent now knows it can:
- Execute Python code for calculations/analysis
- Search the web for current information
- Combine both tools for complex tasks

### Test Results
```
✅ All imports successful
✅ Logging works
✅ Tool registry contains 2 tools
✅ Search web tool works
✅ Execute code tool works
```

### Usage Example

**Before (code execution only):**
```
User: "What's 2+2?"
Agent: Uses execute_code → Returns "4"
```

**Now (code + web search):**
```
User: "What's the latest Python version and what are its new features?"
Agent: 
  1. Uses search_web → Gets current version info
  2. Uses execute_code → Can demonstrate new features
  3. Returns comprehensive answer
```

### API Endpoint Update
`POST /chat` now accepts requests that can:
- Perform calculations via E2B sandboxes
- Search the web via Tavily
- Combine both capabilities intelligently

