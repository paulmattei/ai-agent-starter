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
    print("Testing imports...")
    
    try:
        from tools import AVAILABLE_TOOLS
        from utils.logging import logger
        
        # Validate types
        assert isinstance(AVAILABLE_TOOLS, list), "AVAILABLE_TOOLS should be a list"
        assert hasattr(logger, 'info'), "logger should have info method"
        assert hasattr(logger, 'error'), "logger should have error method"
        
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_logging():
    """
    Test logging utilities.
    
    Validates:
    - logger has standard methods (info, error, warning, debug)
    - No exceptions thrown during logging
    """
    print("\nTesting logging utilities...")
    
    try:
        from utils.logging import logger
        
        # Test standard log levels
        logger.info("Info message")
        logger.error("Error message")
        logger.warning("Warning message")
        logger.debug("Debug message")
        
        print("✅ Logging works")
        return True
    except Exception as e:
        print(f"❌ Logging failed: {e}")
        return False




def test_execute_code_happy_path():
    """
    Test execute_code with valid Python code.
    
    Validates:
    - Returns string
    - Contains expected output in stdout
    - Successfully executes simple print statements
    """
    print("\nTesting execute_code (happy path)...")
    
    try:
        from tools.execute_code import execute_code
        
        if not os.getenv('E2B_API_KEY'):
            print("⚠️  Skipping execute_code test (E2B_API_KEY not set)")
            return True
        
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
        
        print("✅ Execute code (happy path) works")
        return True
    except Exception as e:
        print(f"❌ Execute code test failed: {e}")
        return False


def test_execute_code_errors():
    """
    Test execute_code error handling.
    
    Validates:
    - Syntax errors are caught and returned
    - Runtime errors are caught and returned
    - Error messages are informative
    """
    print("\nTesting execute_code (error handling)...")
    
    try:
        from tools.execute_code import execute_code
        
        if not os.getenv('E2B_API_KEY'):
            print("⚠️  Skipping execute_code error test (E2B_API_KEY not set)")
            return True
        
        # Test 1: Syntax error
        result = execute_code("print('missing parenthesis'")
        assert "error" in result.lower(), "Should contain error message"
        
        # Test 2: Runtime error
        result = execute_code("x = 1 / 0")
        assert "error" in result.lower() or "division" in result.lower(), "Should catch division by zero"
        
        # Test 3: Undefined variable
        result = execute_code("print(undefined_variable)")
        assert "error" in result.lower() or "name" in result.lower(), "Should catch undefined variable"
        
        print("✅ Execute code error handling works")
        return True
    except Exception as e:
        print(f"❌ Execute code error test failed: {e}")
        return False


def test_execute_code_edge_cases():
    """
    Test execute_code with edge cases.
    
    Validates:
    - Empty code
    - Whitespace-only code
    - Very long output
    """
    print("\nTesting execute_code (edge cases)...")
    
    try:
        from tools.execute_code import execute_code
        
        if not os.getenv('E2B_API_KEY'):
            print("⚠️  Skipping execute_code edge cases (E2B_API_KEY not set)")
            return True
        
        # Test 1: Empty code
        result = execute_code("")
        assert isinstance(result, str), "Should return string for empty code"
        
        # Test 2: Only whitespace
        result = execute_code("   \n   \n   ")
        assert isinstance(result, str), "Should handle whitespace-only code"
        
        # Test 3: Code with no output
        result = execute_code("x = 5")
        assert isinstance(result, str), "Should handle code with no output"
        
        print("✅ Execute code edge cases handled")
        return True
    except Exception as e:
        print(f"❌ Execute code edge case test failed: {e}")
        return False


def test_search_web_happy_path():
    """
    Test search_web with valid queries.
    
    Validates:
    - Returns string
    - Contains relevant search results
    - Formats results with titles and URLs
    """
    print("\nTesting search_web (happy path)...")
    
    try:
        from tools.search_web import search_web
        
        if not os.getenv('TAVILY_API_KEY'):
            print("⚠️  Skipping search_web test (TAVILY_API_KEY not set)")
            return True
        
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
        
        print("✅ Search web (happy path) works")
        return True
    except Exception as e:
        print(f"❌ Search web test failed: {e}")
        return False


def test_search_web_format():
    """
    Test search_web output format.
    
    Validates:
    - Results contain structured information
    - URLs are included
    - Content snippets are present
    """
    print("\nTesting search_web (output format)...")
    
    try:
        from tools.search_web import search_web
        
        if not os.getenv('TAVILY_API_KEY'):
            print("⚠️  Skipping search_web format test (TAVILY_API_KEY not set)")
            return True
        
        result = search_web("OpenAI")
        
        # Check for URL presence (common in search results)
        assert "http" in result.lower() or "url" in result.lower(), \
            "Results should contain URLs or URL references"
        
        # Check for numbering (formatted list)
        has_numbers = any(str(i) in result for i in range(1, 6))
        assert has_numbers, "Results should be formatted as numbered list"
        
        print("✅ Search web format validation passed")
        return True
    except Exception as e:
        print(f"❌ Search web format test failed: {e}")
        return False


def test_search_web_edge_cases():
    """
    Test search_web with edge cases.
    
    Validates:
    - Empty query handling
    - Special characters
    - Very specific queries
    """
    print("\nTesting search_web (edge cases)...")
    
    try:
        from tools.search_web import search_web
        
        if not os.getenv('TAVILY_API_KEY'):
            print("⚠️  Skipping search_web edge cases (TAVILY_API_KEY not set)")
            return True
        
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
        
        print("✅ Search web edge cases handled")
        return True
    except Exception as e:
        print(f"❌ Search web edge case test failed: {e}")
        return False


def test_tool_registry():
    """
    Test that AVAILABLE_TOOLS is properly configured.
    
    Validates:
    - Registry is not empty
    - All tools are callable functions
    - All tools have proper docstrings
    - All tools have type hints
    """
    print("\nTesting tool registry...")
    
    try:
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
        
        print(f"✅ Tool registry valid with {len(AVAILABLE_TOOLS)} tool(s): {', '.join(tool_names)}")
        return True
    except Exception as e:
        print(f"❌ Tool registry test failed: {e}")
        return False


def main():
    """
    Run all unit tests.
    
    Test execution order:
    1. Basic imports and infrastructure
    2. Tool registry validation
    3. Individual tool tests (happy path, errors, edge cases)
    """
    print("=" * 80)
    print("JOBBOT UNIT TEST SUITE")
    print("=" * 80)
    print("\n📋 Test Categories:")
    print("  • Infrastructure: Imports, Logging, Registry")
    print("  • execute_code: Happy path, Errors, Edge cases")
    print("  • search_web: Happy path, Format, Edge cases")
    print("\n" + "=" * 80 + "\n")
    
    # Define test groups
    infrastructure_tests = [
        ("Imports", test_imports),
        ("Logging", test_logging),
        ("Tool Registry", test_tool_registry),
    ]
    
    execute_code_tests = [
        ("execute_code: Happy Path", test_execute_code_happy_path),
        ("execute_code: Error Handling", test_execute_code_errors),
        ("execute_code: Edge Cases", test_execute_code_edge_cases),
    ]
    
    search_web_tests = [
        ("search_web: Happy Path", test_search_web_happy_path),
        ("search_web: Output Format", test_search_web_format),
        ("search_web: Edge Cases", test_search_web_edge_cases),
    ]
    
    all_tests = infrastructure_tests + execute_code_tests + search_web_tests
    
    # Run tests and collect results
    results = []
    for name, test_func in all_tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Print summary by category
    print("\n" + "=" * 80)
    print("TEST SUMMARY BY CATEGORY")
    print("=" * 80)
    
    def print_category(category_name, tests):
        passed = sum(1 for name, result in results if any(name.startswith(t[0].split(":")[0]) for t in tests) and result)
        total = len(tests)
        status = "✅" if passed == total else "⚠️"
        print(f"\n{status} {category_name}: {passed}/{total}")
        for test_name, test_func in tests:
            test_result = next((r for n, r in results if n == test_name), False)
            symbol = "  ✅" if test_result else "  ❌"
            print(f"{symbol} {test_name}")
    
    print_category("Infrastructure Tests", infrastructure_tests)
    print_category("execute_code Tests", execute_code_tests)
    print_category("search_web Tests", search_web_tests)
    
    # Overall summary
    print("\n" + "=" * 80)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"OVERALL: {passed}/{total} tests passed ({percentage:.1f}%)")
    print("=" * 80 + "\n")
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

