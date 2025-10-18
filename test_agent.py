"""
End-to-End Test Suite for AI Agent
Tests the full Flask API with HTTP requests to /chat endpoint
"""

import os
import time
import requests
import pytest
from threading import Thread
from dotenv import load_dotenv
from utils.logging import logger

# Load environment variables
load_dotenv()

# Test server configuration
TEST_SERVER_URL = os.getenv("TEST_SERVER_URL", "http://localhost:8080")


def start_test_server():
    """Start the Flask server in a separate thread for testing"""
    from main import app
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)


def wait_for_server(url: str, timeout: int = 10):
    """Wait for the server to be ready"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(f"{url}/health", timeout=1)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False


def chat_request(message: str, model: str = "openai:gpt-4o"):
    """
    Make a request to the /chat endpoint.
    
    Args:
        message: User message
        model: Model to use
        
    Returns:
        Response dict or None if failed
    """
    logger.info("\n" + "=" * 80)
    logger.info(f"📩 HTTP REQUEST to /chat")
    logger.info(f"Message: {message}")
    logger.info(f"Model: {model}")
    logger.info("=" * 80)
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{TEST_SERVER_URL}/chat",
            json={"message": message, "model": model},
            timeout=60  # Allow time for tool execution
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            agent_response = data.get("response", "")
            
            logger.info("=" * 80)
            logger.info(f"✅ HTTP 200 OK (took {elapsed:.2f}s)")
            logger.info(f"Response: {agent_response}")
            logger.info("=" * 80 + "\n")
            
            return data
        else:
            logger.error("=" * 80)
            logger.error(f"❌ HTTP {response.status_code} (took {elapsed:.2f}s)")
            logger.error(f"Error: {response.text}")
            logger.error("=" * 80 + "\n")
            return None
            
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error("=" * 80)
        logger.error(f"❌ REQUEST FAILED (took {elapsed:.2f}s)")
        logger.error(f"Error: {str(e)}")
        logger.error("=" * 80 + "\n")
        return None


def test_health_endpoint():
    """Test: Health endpoint returns 200"""
    response = requests.get(f"{TEST_SERVER_URL}/health", timeout=5)
    logger.info(f"GET /health → HTTP {response.status_code}")
    assert response.status_code == 200


def test_code_execution_task():
    """Test: Agent solves math problem using execute_code via /chat"""
    if not os.getenv('E2B_API_KEY'):
        pytest.skip("E2B_API_KEY not set")
    
    message = "Calculate the first 10 Fibonacci numbers and show them"
    response = chat_request(message)
    
    assert response is not None, "No response received"
    assert "response" in response, "Response missing 'response' field"
    
    answer = response["response"].lower()
    
    # Check that the response contains the Fibonacci sequence
    # Expected: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
    expected_numbers = ["0", "1", "2", "3", "5", "8", "13", "21", "34"]
    
    missing = [num for num in expected_numbers if num not in answer]
    assert len(missing) == 0, f"Response missing expected numbers: {missing}"
    
    logger.info("✅ Response contains correct Fibonacci numbers")


def test_web_search_task():
    """Test: Agent uses web search for current information via /chat"""
    if not os.getenv('TAVILY_API_KEY'):
        pytest.skip("TAVILY_API_KEY not set")
    
    # Use a question that requires current information (stock prices change daily)
    message = "What is the current weather in London? Use web search to get real-time information."
    response = chat_request(message)
    
    assert response is not None, "No response received"
    assert "response" in response, "Response missing 'response' field"
    
    answer = response["response"].lower()
    
    # Check that the response mentions London and weather-related terms
    has_london = "london" in answer
    has_weather_terms = any(term in answer for term in ["weather", "temperature", "celsius", "fahrenheit", "°", "degrees", "cloudy", "sunny", "rain"])
    
    assert has_london, "Response doesn't mention London"
    assert has_weather_terms, "Response doesn't contain weather information"
    
    logger.info("✅ Response contains current weather information from web search")


def test_combined_task():
    """Test: Agent combines web search + code execution via /chat"""
    if not os.getenv('TAVILY_API_KEY'):
        pytest.skip("TAVILY_API_KEY not set")
    if not os.getenv('E2B_API_KEY'):
        pytest.skip("E2B_API_KEY not set")
    
    message = "Search for the population of Tokyo and calculate what 10% of that number is"
    response = chat_request(message)
    
    assert response is not None, "No response received"
    assert "response" in response, "Response missing 'response' field"
    
    answer = response["response"].lower()
    
    # Check that response mentions Tokyo and contains a calculation
    # Should have both search results and computation
    has_tokyo = "tokyo" in answer
    has_numbers = any(char.isdigit() for char in answer)
    has_calculation_terms = any(term in answer for term in ["10%", "percent", "10 percent", "million", "calculated"])
    
    assert has_tokyo, "Response doesn't mention Tokyo"
    assert has_numbers and has_calculation_terms, "Response doesn't show calculation results"
    
    logger.info("✅ Response contains search results and calculation")


def test_complex_code_task():
    """Test: Agent solves complex programming task via /chat"""
    if not os.getenv('E2B_API_KEY'):
        pytest.skip("E2B_API_KEY not set")
    
    message = "Generate a list of the first 5 prime numbers and calculate their sum"
    response = chat_request(message)
    
    assert response is not None, "No response received"
    assert "response" in response, "Response missing 'response' field"
    
    answer = response["response"].lower()
    
    # First 5 primes: 2, 3, 5, 7, 11 (sum = 28)
    # Check for the primes
    expected_primes = ["2", "3", "5", "7", "11"]
    found_primes = sum(1 for prime in expected_primes if prime in answer)
    
    # Check for the sum (28)
    has_sum = "28" in answer
    
    assert found_primes >= 4, f"Response mentions only {found_primes}/5 expected primes"
    assert has_sum, "Response doesn't contain correct sum (28)"
    
    logger.info("✅ Response contains prime numbers and correct sum")


@pytest.fixture(scope="session", autouse=True)
def setup_test_server():
    """Start Flask server before tests if testing locally"""
    if not os.getenv('OPENAI_API_KEY'):
        pytest.exit("OPENAI_API_KEY not set - cannot run E2E tests")
    
    # Start Flask server in background thread (only if testing locally)
    if TEST_SERVER_URL.startswith("http://localhost") or TEST_SERVER_URL.startswith("http://127.0.0.1"):
        logger.info("🚀 Starting Flask server...")
        server_thread = Thread(target=start_test_server, daemon=True)
        server_thread.start()
    
    # Wait for server to be ready
    if not wait_for_server(TEST_SERVER_URL):
        pytest.exit("❌ Server failed to start")
    
    logger.info(f"✅ Server ready at {TEST_SERVER_URL}\n")
    
    yield
    
    # Teardown happens automatically when daemon thread exits
