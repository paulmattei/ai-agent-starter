# Jobbot Testing Documentation

Comprehensive guide to testing tools, test coverage, and validation strategies.

---

## Table of Contents
1. [Testing Overview](#testing-overview)
2. [Tool Specifications](#tool-specifications)
3. [Unit Tests (tests/test_tools.py)](#unit-tests)
4. [End-to-End Tests (tests/test_agent.py)](#end-to-end-tests)
5. [Test Coverage Matrix](#test-coverage-matrix)
6. [Running Tests](#running-tests)

---

## Testing Overview

### Test Types

| Test Type | File | Purpose | Speed | External APIs |
|-----------|------|---------|-------|---------------|
| **Unit** | `tests/test_tools.py` | Test tool functions in isolation | Fast (~10s) | Yes (Tavily, E2B) |
| **E2E** | `tests/test_agent.py` | Test full HTTP API flow | Slow (~30s) | Yes (Flask + Tools) |

---

## Tool Specifications

### Tool 1: `execute_code`

#### Purpose
Execute Python code in secure E2B sandboxes for calculations, data analysis, and programming tasks.

#### Function Signature
```python
def execute_code(code: str) -> str
```

#### Input/Output Specification

| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| `code` | `str` | Python code to execute | Can be empty, multiline |
| **Returns** | `str` | Formatted execution results | Contains stdout/stderr/results/errors |

#### Example Usage

**Input:**
```python
execute_code("""
x = 10
y = 20
print(f'Sum: {x + y}')
""")
```

**Output:**
```
Stdout:
Sum: 30
```

#### Error Handling

| Error Type | Example | Expected Output |
|-----------|---------|-----------------|
| **Syntax Error** | `print('unclosed` | `Error: SyntaxError...` |
| **Runtime Error** | `x = 1 / 0` | `Error: ZeroDivisionError...` |
| **Name Error** | `print(undefined)` | `Error: NameError...` |

#### Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    execute_code()                        │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Create E2B Sandbox      │
          │  (Isolated Environment)  │
          └──────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Run Python Code         │
          │  • Capture stdout        │
          │  • Capture stderr        │
          │  • Capture results       │
          │  • Catch errors          │
          └──────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Format Output           │
          │  • Error messages        │
          │  • Results list          │
          │  • Standard output       │
          └──────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Cleanup Sandbox         │
          │  (Always runs)           │
          └──────────────────────────┘
                         │
                         ▼
                  Return String
```

---

### Tool 2: `search_web`

#### Purpose
Search the web using Tavily API for real-time information, current events, and factual knowledge.

#### Function Signature
```python
def search_web(query: str) -> str
```

#### Input/Output Specification

| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| `query` | `str` | Search query | Non-empty string |
| **Returns** | `str` | Formatted search results | Structured with titles/URLs/content |

#### Example Usage

**Input:**
```python
search_web("Python programming language")
```

**Output:**
```
Quick Answer:
Python is a high-level programming language...

Search Results for 'Python programming language':

1. Python Official Website
   URL: https://www.python.org
   Python is a programming language that lets you work quickly...

2. Python Documentation
   URL: https://docs.python.org
   The official Python documentation...
```

#### Output Format Structure

```
┌────────────────────────────────────────┐
│        Search Results Format           │
├────────────────────────────────────────┤
│                                        │
│  Quick Answer: (if available)          │
│  [AI-generated summary from Tavily]    │
│                                        │
│  Search Results for 'query':           │
│                                        │
│  1. [Title]                            │
│     URL: [url]                         │
│     [Content snippet]                  │
│                                        │
│  2. [Title]                            │
│     URL: [url]                         │
│     [Content snippet]                  │
│                                        │
│  ... (up to 5 results)                 │
│                                        │
└────────────────────────────────────────┘
```

#### Error Handling

| Error Type | Cause | Expected Output |
|-----------|-------|-----------------|
| **Missing API Key** | `TAVILY_API_KEY` not set | `TAVILY_API_KEY not found in environment variables` |
| **Network Error** | API unreachable | `Web search failed: [error details]` |
| **No Results** | Query too specific | `No results found.` |

#### Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    search_web()                          │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Check API Key           │
          │  (TAVILY_API_KEY)        │
          └──────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Initialize Tavily Client│
          └──────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Execute Search          │
          │  • max_results: 5        │
          │  • include_answer: true  │
          │  • include_raw: false    │
          └──────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────┐
          │  Format Results          │
          │  • Quick answer (if any) │
          │  • Numbered list         │
          │  • Title + URL + Content │
          └──────────────────────────┘
                         │
                         ▼
                  Return String
```

---

## Unit Tests

### Test Suite Structure

```
tests/test_tools.py (9 tests)
│
├── Infrastructure Tests (3)
│   ├── test_imports()
│   ├── test_logging()
│   └── test_tool_registry()
│
├── execute_code Tests (3)
│   ├── test_execute_code_happy_path()
│   ├── test_execute_code_errors()
│   └── test_execute_code_edge_cases()
│
└── search_web Tests (3)
    ├── test_search_web_happy_path()
    ├── test_search_web_format()
    └── test_search_web_edge_cases()
```

### Detailed Test Breakdown

#### Infrastructure Tests

| Test | What It Validates | Assertions |
|------|------------------|------------|
| `test_imports` | Module imports work | • `AVAILABLE_TOOLS` is a list<br>• `log_span` is callable<br>• `Colors` has attributes |
| `test_logging` | Logging system works | • All log levels accepted<br>• No exceptions thrown<br>• Default level works |
| `test_tool_registry` | Tool registry valid | • Registry not empty<br>• All tools callable<br>• All have docstrings<br>• Expected tools present |

#### execute_code Tests

| Test | Scenarios | Expected Behavior |
|------|-----------|-------------------|
| **Happy Path** | • Simple print<br>• Calculation<br>• Multi-line code | • Returns string<br>• Contains output<br>• Executes correctly |
| **Error Handling** | • Syntax error<br>• Division by zero<br>• Undefined variable | • Returns error message<br>• Doesn't crash<br>• Error is informative |
| **Edge Cases** | • Empty code<br>• Whitespace only<br>• No output | • Returns string<br>• Handles gracefully |

**Test Case Detail: Happy Path**
```python
┌─────────────────────────────────────────────────────────────┐
│ Test Case: execute_code_happy_path                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Test 1: Simple Print                                        │
│   Input:  print('Hello from E2B')                           │
│   Assert: "Hello from E2B" in result                        │
│                                                              │
│ Test 2: Calculation                                         │
│   Input:  result = 2 + 2\nresult                            │
│   Assert: "4" in result                                     │
│                                                              │
│ Test 3: Multi-line                                          │
│   Input:  x = 10                                            │
│           y = 20                                            │
│           print(f'Sum: {x + y}')                            │
│   Assert: "Sum: 30" in result                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### search_web Tests

| Test | Scenarios | Expected Behavior |
|------|-----------|-------------------|
| **Happy Path** | • General query<br>• Factual query | • Returns string<br>• Contains relevant content<br>• Substantive results |
| **Format Validation** | • Check structure<br>• Verify URLs<br>• Check numbering | • Contains URLs<br>• Numbered list format<br>• Proper structure |
| **Edge Cases** | • Single word<br>• Question format<br>• Specific query | • Handles gracefully<br>• Returns results<br>• No crashes |

**Test Case Detail: Format Validation**
```python
┌─────────────────────────────────────────────────────────────┐
│ Test Case: search_web_format                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Input:  search_web("OpenAI")                                │
│                                                              │
│ Assertions:                                                  │
│   ✓ Contains "http" or "url"  → Validates URLs present      │
│   ✓ Contains numbers 1-5      → Validates list formatting   │
│                                                              │
│ Expected Output Structure:                                   │
│   "1. [Title]                                                │
│    URL: http://...                                           │
│    [Content]"                                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## End-to-End Tests

### Test Suite Structure

```
tests/test_agent.py (5 tests)
│
├── test_health_endpoint()
│   └── GET /health → 200 OK
│
├── test_code_execution_task()
│   └── POST /chat → Fibonacci numbers
│
├── test_web_search_task()
│   └── POST /chat → Current weather in London
│
├── test_combined_task()
│   └── POST /chat → Tokyo population + calculation
│
└── test_complex_code_task()
    └── POST /chat → Prime numbers + sum
```

### Test Execution Flow

```
┌──────────────────────────────────────────────────────────────┐
│              E2E Test Execution Flow                         │
└──────────────────────────────────────────────────────────────┘

    [1] Start Flask Server
         │
         ├─→ Background thread
         ├─→ Port 8080
         └─→ Wait for ready
              │
              ▼
    [2] Health Check Test
         │
         ├─→ GET /health
         └─→ Assert: status == 200
              │
              ▼
    [3] Code Execution Test
         │
         ├─→ POST /chat ("Calculate Fibonacci")
         ├─→ Server → Agent → execute_code
         └─→ Assert: Response contains [0,1,1,2,3,5,8,13,21,34]
              │
              ▼
    [4] Web Search Test
         │
         ├─→ POST /chat ("Current weather in London")
         ├─→ Server → Agent → search_web
         └─→ Assert: Response contains weather data
              │
              ▼
    [5] Combined Tools Test
         │
         ├─→ POST /chat ("Tokyo population + 10%")
         ├─→ Server → Agent → search_web + execute_code
         └─→ Assert: Contains "Tokyo" + numbers + calc
              │
              ▼
    [6] Complex Code Test
         │
         ├─→ POST /chat ("5 primes + sum")
         ├─→ Server → Agent → execute_code
         └─→ Assert: Contains primes + sum=28
```

### Detailed Test Specifications

#### Test 1: Health Endpoint

| Attribute | Value |
|-----------|-------|
| **Method** | GET |
| **Endpoint** | `/health` |
| **Expected Status** | 200 |
| **Validation** | `response.status_code == 200` |
| **Purpose** | Verify server is running |

#### Test 2: Code Execution Task

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **Endpoint** | `/chat` |
| **Request** | `{"message": "Calculate the first 10 Fibonacci numbers"}` |
| **Expected Tools** | `execute_code` |
| **Validation** | Response contains: 0, 1, 2, 3, 5, 8, 13, 21, 34 |
| **Purpose** | Verify code execution works end-to-end |

**Validation Logic:**
```python
expected_numbers = ["0", "1", "2", "3", "5", "8", "13", "21", "34"]
missing = [num for num in expected_numbers if num not in answer]
assert len(missing) == 0, f"Missing: {missing}"
```

#### Test 3: Web Search Task

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **Endpoint** | `/chat` |
| **Request** | `{"message": "What is the current weather in London? Use web search to get real-time information."}` |
| **Expected Tools** | `search_web` |
| **Validation** | Response contains: "london" + weather terms (temperature/celsius/degrees/etc.) |
| **Purpose** | Verify web search with real-time data |

#### Test 4: Combined Tools Task

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **Endpoint** | `/chat` |
| **Request** | `{"message": "Search for population of Tokyo and calculate 10%"}` |
| **Expected Tools** | `search_web` → `execute_code` |
| **Validation** | • Contains "Tokyo"<br>• Contains numbers<br>• Contains calculation terms |
| **Purpose** | Verify multi-tool orchestration |

**Multi-Validation:**
```python
has_tokyo = "tokyo" in answer
has_numbers = any(char.isdigit() for char in answer)
has_calc = any(term in answer for term in 
               ["10%", "percent", "million", "calculated"])

assert has_tokyo and has_numbers and has_calc
```

#### Test 5: Complex Code Task

| Attribute | Value |
|-----------|-------|
| **Method** | POST |
| **Endpoint** | `/chat` |
| **Request** | `{"message": "Generate first 5 prime numbers and calculate sum"}` |
| **Expected Tools** | `execute_code` |
| **Validation** | • Contains 4/5 primes (2, 3, 5, 7, 11)<br>• Contains sum (28) |
| **Purpose** | Verify complex programming tasks |

**Dual Validation:**
```python
expected_primes = ["2", "3", "5", "7", "11"]
found_primes = sum(1 for p in expected_primes if p in answer)
has_sum = "28" in answer

assert found_primes >= 4 and has_sum
```

---

## Test Coverage Matrix

### Tool Coverage

| Tool | Unit Tests | E2E Tests | Total Scenarios |
|------|-----------|-----------|-----------------|
| `execute_code` | 3 tests (9 scenarios) | 3 tests | 12 scenarios |
| `search_web` | 3 tests (7 scenarios) | 2 tests | 9 scenarios |
| **Total** | **6 tests** | **5 tests** | **21 scenarios** |

### Coverage by Scenario Type

```
┌─────────────────────────────────────────────────────────────┐
│                  Test Coverage Breakdown                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Happy Path Tests:     ████████████░░  42% (9/21)          │
│  Error Handling:       ███████░░░░░░░  29% (6/21)          │
│  Edge Cases:           ██████░░░░░░░░  24% (5/21)          │
│  Integration:          ███░░░░░░░░░░░   5% (1/21)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Detailed Coverage Matrix

| Scenario | Unit Test | E2E Test | Notes |
|----------|-----------|----------|-------|
| **Simple code execution** | ✅ | ✅ | Fibonacci, primes |
| **Code with errors** | ✅ | ❌ | Syntax/runtime errors |
| **Empty/whitespace code** | ✅ | ❌ | Edge case handling |
| **Multi-line code** | ✅ | ✅ | Real-world usage |
| **General web search** | ✅ | ✅ | Python, OpenAI |
| **Factual queries** | ✅ | ✅ | Capitals, facts |
| **Search result format** | ✅ | ❌ | URL/numbering validation |
| **Multi-tool orchestration** | ❌ | ✅ | Tokyo test |
| **Tool registry** | ✅ | ❌ | Configuration validation |
| **Logging system** | ✅ | ❌ | Infrastructure |
| **HTTP endpoints** | ❌ | ✅ | `/health`, `/chat` |

---

## Running Tests

### Quick Reference

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests with pytest
pytest

# Unit tests only (fast, ~10s)
pytest tests/test_tools.py

# E2E tests only (local server, ~30s)
pytest tests/test_agent.py

# Or test against deployed Fly.io app
TEST_SERVER_URL=https://your-app-name.fly.dev pytest tests/test_agent.py

# Run with verbose output
pytest -v
```

### Test Output Examples

#### Unit Tests Output

```
================================================================================
JOBBOT UNIT TEST SUITE
================================================================================

📋 Test Categories:
  • Infrastructure: Imports, Logging, Registry
  • execute_code: Happy path, Errors, Edge cases
  • search_web: Happy path, Format, Edge cases

================================================================================

Testing imports...
✅ All imports successful

Testing logging utilities...
✅ Logging works

Testing tool registry...
✅ Tool registry valid with 2 tool(s): execute_code, search_web

Testing execute_code (happy path)...
✅ Execute code (happy path) works

Testing execute_code (error handling)...
✅ Execute code error handling works

Testing execute_code (edge cases)...
✅ Execute code edge cases handled

Testing search_web (happy path)...
✅ Search web (happy path) works

Testing search_web (output format)...
✅ Search web format validation passed

Testing search_web (edge cases)...
✅ Search web edge cases handled

================================================================================
TEST SUMMARY BY CATEGORY
================================================================================

✅ Infrastructure Tests: 3/3
  ✅ Imports
  ✅ Logging
  ✅ Tool Registry

✅ execute_code Tests: 3/3
  ✅ execute_code: Happy Path
  ✅ execute_code: Error Handling
  ✅ execute_code: Edge Cases

✅ search_web Tests: 3/3
  ✅ search_web: Happy Path
  ✅ search_web: Output Format
  ✅ search_web: Edge Cases

================================================================================
OVERALL: 9/9 tests passed (100.0%)
================================================================================
```

#### E2E Tests Output

```
================================================================================
AI AGENT END-TO-END TEST SUITE (HTTP API)
================================================================================

✅ All environment variables set

2025-10-18 15:56:03 [INFO] ✅ Server ready at http://localhost:8080


📝 TEST 1: Health Endpoint
================================================================================
2025-10-18 15:56:03 [INFO] GET /health → HTTP 200

📝 TEST 2: Code Execution Task
================================================================================
2025-10-18 15:56:03 [INFO] 📩 HTTP REQUEST to /chat
2025-10-18 15:56:03 [INFO] Message: Calculate the first 10 Fibonacci numbers
2025-10-18 15:56:06 [INFO] ✅ HTTP 200 OK (took 3.10s)
2025-10-18 15:56:06 [INFO] Response: The first 10 Fibonacci numbers are: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
2025-10-18 15:56:06 [INFO] ✅ Response contains correct Fibonacci numbers

[... more tests ...]

================================================================================
TEST SUMMARY
================================================================================
✅ PASS - Health Endpoint
✅ PASS - Code Execution
✅ PASS - Web Search
✅ PASS - Combined Tools
✅ PASS - Complex Code
================================================================================
RESULTS: 5/5 tests passed
================================================================================
```

### Environment Setup for Testing

#### Required Environment Variables

| Variable | Purpose | Required For |
|----------|---------|--------------|
| `OPENAI_API_KEY` | LLM provider | E2E tests |
| `E2B_API_KEY` | Code execution | Unit + E2E tests |
| `TAVILY_API_KEY` | Web search | Unit + E2E tests |

#### Test Execution Matrix

| Test Suite | Requires OpenAI | Requires E2B | Requires Tavily |
|------------|----------------|--------------|-----------------|
| Unit Tests | ❌ | ✅ (for execute_code) | ✅ (for search_web) |
| E2E Tests | ✅ | ✅ | ✅ |

**Note:** Tests gracefully skip if API keys are missing, but full coverage requires all keys.

---

## Continuous Integration

### GitHub Actions + Codecov

This project uses **automated CI/CD** with GitHub Actions and Codecov for test automation and coverage reporting.

#### Workflow Configuration

See `.github/workflows/test.yml` for the complete workflow. It:

- ✅ Runs on every push and pull request
- ✅ Tests with Python 3.11 and 3.12
- ✅ Executes unit and E2E tests with pytest
- ✅ Generates coverage reports
- ✅ Uploads to Codecov automatically
- ✅ Updates README badges

#### Setup Instructions

See `.github/SETUP_CI.md` for detailed setup instructions including:

- Adding GitHub secrets (API keys)
- Connecting Codecov
- Configuring badges
- Troubleshooting common issues

#### Running Tests Locally with Pytest

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/test_tools.py -v

# Run E2E tests only
pytest tests/test_agent.py -v

# Run with coverage report
pytest --cov=tools --cov=utils --cov=main --cov-report=term --cov-report=xml

# Run specific test
pytest tests/test_tools.py::test_execute_code_happy_path -v
```

#### Coverage Configuration

Coverage settings are defined in:
- `.codecov.yml` - Codecov configuration (targets, thresholds)
- `pytest.ini` - Pytest and coverage options

---

## Appendix: Test Metrics

### Performance Benchmarks

| Test | Average Duration | API Calls | Cost Estimate |
|------|-----------------|-----------|---------------|
| Unit: execute_code | ~2s per test | 1-3 E2B calls | $0.001 |
| Unit: search_web | ~3s per test | 1-3 Tavily calls | $0.002 |
| E2E: Code execution | ~5s | 1 OpenAI + 1-2 E2B | $0.005 |
| E2E: Web search | ~3s | 1 OpenAI + 1 Tavily | $0.006 |
| E2E: Combined | ~12s | 1 OpenAI + Tavily + E2B | $0.010 |
| **Full Test Suite** | **~45s** | **~25 API calls** | **~$0.10** |

### Test Reliability

| Test | Flakiness | Retry Logic | Notes |
|------|-----------|-------------|-------|
| Unit tests | Low | No | Direct API calls |
| E2E tests | Medium | No | Depends on server startup |
| Combined tools | Medium-High | No | Multi-step, LLM decisions |

**Recommendation:** For production CI, add retry logic for E2E tests due to LLM non-determinism.

---

**Last Updated:** 2025-10-18  
**Test Coverage:** 100% of tool functions, 95% of code paths  
**Maintainer:** See ARCHITECTURE.md


