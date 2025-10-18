"""
Logging utilities for the jobbot application.
Provides colored terminal output with timestamps.
"""

from datetime import datetime


class Colors:
    """ANSI color codes for terminal tracing"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def log_span(message: str, level: str = "info"):
    """
    Print a traced span with timestamp and color.
    
    Args:
        message (str): The message to log
        level (str): Log level (info, success, error, tool)
    """
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    
    color_map = {
        "info": Colors.BLUE,
        "success": Colors.GREEN,
        "error": Colors.RED,
        "tool": Colors.YELLOW
    }
    
    color = color_map.get(level, Colors.RESET)
    print(f"{color}[{timestamp}] {message}{Colors.RESET}")

