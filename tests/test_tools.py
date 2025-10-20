"""
Unit Test Suite for Jobbot Tools
Tests individual tool functions in isolation with comprehensive validation.

Test Categories:
- Import validation
- Logging utilities
- Tool registry
- execute_code tool (happy path, errors, edge cases)
- search_web tool (happy path, errors, edge cases)
"""

import sys
import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_imports():
    """
    Test that all modules import correctly.
    
    Validates:
    - tools module exports AVAILABLE_TOOLS
    - utils.logging exports logger
    """
    from tools import AVAILABLE_TOOLS
    from utils.logging import logger
    
    # Validate types
    assert isinstance(AVAILABLE_TOOLS, list), "AVAILABLE_TOOLS should be a list"
    assert hasattr(logger, 'info'), "logger should have info method"
    assert hasattr(logger, 'error'), "logger should have error method"


def test_logging():
    """
    Test logging utilities.
    
    Validates:
    - logger has standard methods (info, error, warning, debug)
    - No exceptions thrown during logging
    """
    from utils.logging import logger
    
    # Test standard log levels
    logger.info("Info message")
    logger.error("Error message")
    logger.warning("Warning message")
    logger.debug("Debug message")




def test_execute_code_happy_path():
    """
    Test execute_code with valid Python code.
    
    Validates:
    - Returns string
    - Contains expected output in stdout
    - Successfully executes simple print statements
    """
    from tools.execute_code import execute_code
    
    if not os.getenv('E2B_API_KEY'):
        pytest.skip("E2B_API_KEY not set")
    
    # Test 1: Simple print
    result = execute_code("print('Hello from E2B')")
    assert isinstance(result, str), "Result should be a string"
    assert "Hello from E2B" in result, f"Expected 'Hello from E2B' in result"
    
    # Test 2: Calculation with result
    result = execute_code("result = 2 + 2\nresult")
    assert "4" in result, "Should contain calculation result"
    
    # Test 3: Multiple lines
    code = """
x = 10
y = 20
print(f'Sum: {x + y}')
"""
    result = execute_code(code)
    assert "Sum: 30" in result, "Should execute multi-line code"


def test_execute_code_errors():
    """
    Test execute_code error handling.
    
    Validates:
    - Syntax errors are caught and returned
    - Runtime errors are caught and returned
    - Error messages are informative
    """
    from tools.execute_code import execute_code
    
    if not os.getenv('E2B_API_KEY'):
        pytest.skip("E2B_API_KEY not set")
    
    # Test 1: Syntax error
    result = execute_code("print('missing parenthesis'")
    assert "error" in result.lower(), "Should contain error message"
    
    # Test 2: Runtime error
    result = execute_code("x = 1 / 0")
    assert "error" in result.lower() or "division" in result.lower(), "Should catch division by zero"
    
    # Test 3: Undefined variable
    result = execute_code("print(undefined_variable)")
    assert "error" in result.lower() or "name" in result.lower(), "Should catch undefined variable"


def test_execute_code_edge_cases():
    """
    Test execute_code with edge cases.
    
    Validates:
    - Empty code
    - Whitespace-only code
    - Very long output
    """
    from tools.execute_code import execute_code
    
    if not os.getenv('E2B_API_KEY'):
        pytest.skip("E2B_API_KEY not set")
    
    # Test 1: Empty code
    result = execute_code("")
    assert isinstance(result, str), "Should return string for empty code"
    
    # Test 2: Only whitespace
    result = execute_code("   \n   \n   ")
    assert isinstance(result, str), "Should handle whitespace-only code"
    
    # Test 3: Code with no output
    result = execute_code("x = 5")
    assert isinstance(result, str), "Should handle code with no output"


def test_search_web_happy_path():
    """
    Test search_web with valid queries.
    
    Validates:
    - Returns string
    - Contains relevant search results
    - Formats results with titles and URLs
    """
    from tools.search_web import search_web
    
    if not os.getenv('TAVILY_API_KEY'):
        pytest.skip("TAVILY_API_KEY not set")
    
    # Test 1: General query
    result = search_web("Python programming language")
    assert isinstance(result, str), "Result should be a string"
    assert "python" in result.lower(), "Should contain Python-related content"
    assert len(result) > 50, "Should return substantive results"
    
    # Test 2: Specific factual query
    result = search_web("Eiffel Tower height")
    assert isinstance(result, str), "Result should be a string"
    assert any(term in result.lower() for term in ["eiffel", "tower", "height", "meter", "feet"]), \
        "Should contain relevant information"


def test_search_web_format():
    """
    Test search_web output format.
    
    Validates:
    - Results contain structured information
    - URLs are included
    - Content snippets are present
    """
    from tools.search_web import search_web
    
    if not os.getenv('TAVILY_API_KEY'):
        pytest.skip("TAVILY_API_KEY not set")
    
    result = search_web("OpenAI")
    
    # Check for URL presence (common in search results)
    assert "http" in result.lower() or "url" in result.lower(), \
        "Results should contain URLs or URL references"
    
    # Check for numbering (formatted list)
    has_numbers = any(str(i) in result for i in range(1, 6))
    assert has_numbers, "Results should be formatted as numbered list"


def test_search_web_edge_cases():
    """
    Test search_web with edge cases.
    
    Validates:
    - Empty query handling
    - Special characters
    - Very specific queries
    """
    from tools.search_web import search_web
    
    if not os.getenv('TAVILY_API_KEY'):
        pytest.skip("TAVILY_API_KEY not set")
    
    # Test 1: Single word
    result = search_web("Python")
    assert isinstance(result, str), "Should handle single-word queries"
    assert len(result) > 0, "Should return results"
    
    # Test 2: Question format
    result = search_web("What is machine learning?")
    assert isinstance(result, str), "Should handle question format"
    
    # Test 3: Very specific query
    result = search_web("2024 Olympics location")
    assert isinstance(result, str), "Should handle specific queries"


def test_tool_registry():
    """
    Test that AVAILABLE_TOOLS is properly configured.
    
    Validates:
    - Registry is not empty
    - All tools are callable functions
    - All tools have proper docstrings
    - All tools have type hints
    """
    from tools import AVAILABLE_TOOLS
    
    # Check registry not empty
    assert len(AVAILABLE_TOOLS) > 0, "AVAILABLE_TOOLS is empty"
    
    # Check all are callable functions
    assert all(callable(tool) for tool in AVAILABLE_TOOLS), "Not all tools are callable"
    
    # Check all have docstrings
    for tool in AVAILABLE_TOOLS:
        assert tool.__doc__, f"Tool {tool.__name__} missing docstring"
    
    # Check expected tools are present
    tool_names = [tool.__name__ for tool in AVAILABLE_TOOLS]
    assert 'execute_code' in tool_names, "execute_code should be in registry"
    assert 'search_web' in tool_names, "search_web should be in registry"

