"""
Code execution tool using E2B sandboxes.
Provides safe Python code execution in isolated environments.
"""

from e2b_code_interpreter import Sandbox
from utils.logging import logger


def execute_code(code: str) -> str:
    """
    Execute code in E2B sandbox.
    
    Args:
        code (str): The Python code to execute
        
    Returns:
        str: Execution results including stdout, stderr, and any errors
    """
    logger.info("🔧 Executing code in E2B sandbox...")
    logger.info(f"Code: {code}")
    
    try:
        sandbox = Sandbox.create()
        logger.info("✓ Sandbox created")
        
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
        
            logger.info(f"✓ Execution completed: {result[:100]}...")
            return result
            
        finally:
            sandbox.kill()
            logger.info("✓ Sandbox cleaned up")
    
    except Exception as e:
        error_msg = f"Sandbox execution failed: {str(e)}"
        logger.error(f"✗ {error_msg}")
        return error_msg

