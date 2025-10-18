"""
End-to-End Test Suite for AI Agent
Tests the full Flask API with HTTP requests to /chat endpoint
"""

import os
import time
import requests
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
    print("\n📝 TEST 1: Health Endpoint")
    print("=" * 80)
    
    try:
        response = requests.get(f"{TEST_SERVER_URL}/health", timeout=5)
        logger.info(f"GET /health → HTTP {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False


def test_code_execution_task():
    """Test: Agent solves math problem using execute_code via /chat"""
    print("\n📝 TEST 2: Code Execution Task")
    print("=" * 80)
    
    message = "Calculate the first 10 Fibonacci numbers and show them"
    response = chat_request(message)
    
    if not response or "response" not in response:
        logger.error("❌ No response received")
        return False
    
    answer = response["response"].lower()
    
    # Check that the response contains the Fibonacci sequence
    # Expected: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
    expected_numbers = ["0", "1", "2", "3", "5", "8", "13", "21", "34"]
    
    missing = [num for num in expected_numbers if num not in answer]
    if missing:
        logger.error(f"❌ Response missing expected numbers: {missing}")
        logger.error(f"Response was: {answer[:200]}")
        return False
    
    logger.info("✅ Response contains correct Fibonacci numbers")
    return True


def test_web_search_task():
    """Test: Agent uses web search for current information via /chat"""
    print("\n📝 TEST 3: Web Search Task")
    print("=" * 80)
    
    if not os.getenv('TAVILY_API_KEY'):
        logger.info("⏭️  Skipping web search test (TAVILY_API_KEY not set)")
        return True
    
    # Use a question that requires current information (stock prices change daily)
    message = "What is the current weather in London? Use web search to get real-time information."
    response = chat_request(message)
    
    if not response or "response" not in response:
        logger.error("❌ No response received")
        return False
    
    answer = response["response"].lower()
    
    # Check that the response mentions London and weather-related terms
    has_london = "london" in answer
    has_weather_terms = any(term in answer for term in ["weather", "temperature", "celsius", "fahrenheit", "°", "degrees", "cloudy", "sunny", "rain"])
    
    if not has_london:
        logger.error("❌ Response doesn't mention London")
        logger.error(f"Response was: {answer[:200]}")
        return False
    
    if not has_weather_terms:
        logger.error("❌ Response doesn't contain weather information")
        logger.error(f"Response was: {answer[:200]}")
        return False
    
    logger.info("✅ Response contains current weather information from web search")
    return True


def test_combined_task():
    """Test: Agent combines web search + code execution via /chat"""
    print("\n📝 TEST 4: Combined Task (Search + Code)")
    print("=" * 80)
    
    if not os.getenv('TAVILY_API_KEY'):
        logger.info("⏭️  Skipping combined test (TAVILY_API_KEY not set)")
        return True
    
    message = "Search for the population of Tokyo and calculate what 10% of that number is"
    response = chat_request(message)
    
    if not response or "response" not in response:
        logger.error("❌ No response received")
        return False
    
    answer = response["response"].lower()
    
    # Check that response mentions Tokyo and contains a calculation
    # Should have both search results and computation
    has_tokyo = "tokyo" in answer
    has_numbers = any(char.isdigit() for char in answer)
    has_calculation_terms = any(term in answer for term in ["10%", "percent", "10 percent", "million", "calculated"])
    
    if not has_tokyo:
        logger.error("❌ Response doesn't mention Tokyo")
        logger.error(f"Response was: {answer[:200]}")
        return False
    
    if not (has_numbers and has_calculation_terms):
        logger.error("❌ Response doesn't show calculation results")
        logger.error(f"Response was: {answer[:200]}")
        return False
    
    logger.info("✅ Response contains search results and calculation")
    return True


def test_complex_code_task():
    """Test: Agent solves complex programming task via /chat"""
    print("\n📝 TEST 5: Complex Code Task")
    print("=" * 80)
    
    message = "Generate a list of the first 5 prime numbers and calculate their sum"
    response = chat_request(message)
    
    if not response or "response" not in response:
        logger.error("❌ No response received")
        return False
    
    answer = response["response"].lower()
    
    # First 5 primes: 2, 3, 5, 7, 11 (sum = 28)
    # Check for the primes
    expected_primes = ["2", "3", "5", "7", "11"]
    found_primes = sum(1 for prime in expected_primes if prime in answer)
    
    # Check for the sum (28)
    has_sum = "28" in answer
    
    if found_primes < 4:  # At least 4 out of 5 primes should be mentioned
        logger.error(f"❌ Response mentions only {found_primes}/5 expected primes")
        logger.error(f"Response was: {answer[:200]}")
        return False
    
    if not has_sum:
        logger.error("❌ Response doesn't contain correct sum (28)")
        logger.error(f"Response was: {answer[:200]}")
        return False
    
    logger.info("✅ Response contains prime numbers and correct sum")
    return True


if __name__ == "__main__":
    # Check environment variables
    required_vars = ['OPENAI_API_KEY', 'E2B_API_KEY']
    optional_vars = ['TAVILY_API_KEY']
    
    missing_required = [var for var in required_vars if not os.getenv(var)]
    missing_optional = [var for var in optional_vars if not os.getenv(var)]
    
    print("\n" + "=" * 80)
    print("AI AGENT END-TO-END TEST SUITE (HTTP API)")
    print("=" * 80)
    
    if missing_required:
        print(f"\n❌ Missing required variables: {', '.join(missing_required)}")
        print("Cannot run tests. Please set them in your .env file\n")
        exit(1)
    
    if missing_optional:
        print(f"\n⚠️  Missing optional variables: {', '.join(missing_optional)}")
        print("Some tests will be skipped\n")
    else:
        print("\n✅ All environment variables set\n")
    
    # Start Flask server in background thread (only if testing locally)
    if TEST_SERVER_URL.startswith("http://localhost") or TEST_SERVER_URL.startswith("http://127.0.0.1"):
        logger.info("🚀 Starting Flask server...")
        server_thread = Thread(target=start_test_server, daemon=True)
        server_thread.start()
    
    # Wait for server to be ready
    if not wait_for_server(TEST_SERVER_URL):
        logger.error("❌ Server failed to start")
        exit(1)
    
    logger.info(f"✅ Server ready at {TEST_SERVER_URL}\n")
    
    # Run test suite
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Code Execution", test_code_execution_task),
        ("Web Search", test_web_search_task),
        ("Combined Tools", test_combined_task),
        ("Complex Code", test_complex_code_task),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 80)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 80 + "\n")
    
    exit(0 if passed == total else 1)
