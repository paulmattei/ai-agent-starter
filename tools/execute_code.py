"""
Code execution tool using E2B sandboxes.
Provides safe Python code execution in isolated environments.
"""

from e2b_code_interpreter import Sandbox
from utils.logging import log_span


def execute_code(code: str) -> str:
    """
    Execute code in E2B sandbox.
    
    Args:
        code (str): The Python code to execute
        
    Returns:
        str: Execution results including stdout, stderr, and any errors
    """
    log_span("🔧 Executing code in E2B sandbox...", "tool")
    log_span(f"Code: {code}", "tool")
    
    try:
        sandbox = Sandbox.create()
        log_span("✓ Sandbox created", "tool")
        
        try:
            execution = sandbox.run_code(code)
            
            # Build result string from execution
            result_parts = []
            
            if execution.error:
                result_parts.append(f"Error: {execution.error}")
            
            if execution.results:
                result_parts.append(f"Results: {execution.results}")
            
            if execution.logs.stdout:
                result_parts.append(f"Stdout:\n{execution.logs.stdout}")
            
            if execution.logs.stderr:
                result_parts.append(f"Stderr:\n{execution.logs.stderr}")
            
            result = "\n".join(result_parts) if result_parts else "Code executed successfully with no output"
        
            log_span(f"✓ Execution completed: {result[:100]}...", "tool")
            return result
            
        finally:
            sandbox.kill()
            log_span("✓ Sandbox cleaned up", "tool")
    
    except Exception as e:
        error_msg = f"Sandbox execution failed: {str(e)}"
        log_span(f"✗ {error_msg}", "error")
        return error_msg

