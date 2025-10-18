"""
AI Agent with Tool Calling
Simple agent using aisuite with E2B code execution
"""

import os
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import aisuite as ai

# Import tools and utilities
from tools import AVAILABLE_TOOLS
from utils.logging import log_span

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize clients
aisuite_client = ai.Client()
        

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint for the AI agent.
    
    Expected JSON body:
    {
        "message": "user message here",
        "model": "openai:gpt-4o" (optional, defaults to gpt-4o)
    }
    """
    request_start = time.time()
    
    try:
        data = request.json
        user_message = data.get('message', '')
        model = data.get('model', 'openai:gpt-4o')
        
        # Log request start
        log_span("\n" + "=" * 80, "info")
        log_span("📩 NEW CHAT REQUEST", "info")
        log_span(f"Model: {model}", "info")
        log_span(f"Message: {user_message}", "info")
        log_span("=" * 80, "info")

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
        
        If you cannot solve the problem with available tools, explain what information is missing.
        "

        """
        
        # Define available tools
        tools = AVAILABLE_TOOLS
        
        # Log agent call start
        log_span("🤖 Starting AI agent processing...", "info")

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        # Call agent with tools
        # Using aisuite's automatic tool execution with max_turns
        response = aisuite_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            max_turns=3  # Allow up to 3 tool calling iterations
        )
        
        # Extract response
        agent_response = response.choices[0].message.content
        
        # Log request completion
        total_time = time.time() - request_start
        log_span("=" * 80, "success")
        log_span(f"✅ CHAT REQUEST COMPLETED (total: {total_time:.2f}s)", "success")
        log_span(f"Response: {agent_response}", "success")
        log_span("=" * 80 + "\n", "success")
        
        # Return response
        return jsonify({
            "response": agent_response,
            "model": model
        }), 200
        
    except Exception as e:
        # Log error
        total_time = time.time() - request_start
        log_span("=" * 80, "error")
        log_span(f"❌ CHAT REQUEST FAILED (total: {total_time:.2f}s)", "error")
        log_span(f"Error: {str(e)}", "error")
        log_span("=" * 80 + "\n", "error")
        
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    """Welcome endpoint with usage instructions"""
    return jsonify({
        "service": "AI Agent with Code Execution",
        "version": "1.0.0",
        "endpoints": {
            "/health": "GET - Health check",
            "/chat": "POST - Chat with agent (requires 'message' in JSON body)",
        },
        "example": {
            "url": "/chat",
            "method": "POST",
            "body": {
                "message": "Write Python code to calculate the first 10 Fibonacci numbers",
                "model": "openai:gpt-4o"
            }
        }
    }), 200


if __name__ == '__main__':
    # Check required environment variables
    required_vars = ['OPENAI_API_KEY', 'E2B_API_KEY', 'TAVILY_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in .env file or environment")
    
    # Run Flask app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

