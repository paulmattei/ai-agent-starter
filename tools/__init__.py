"""
Tool registry for the jobbot AI agent.
Provides a central location for all available tools.
"""

from .execute_code import execute_code
from .search_web import search_web

# Registry of all available tools
# Add or remove tools here to make them available to the AI agent
AVAILABLE_TOOLS = [
    execute_code,
    search_web,
]

__all__ = [
    "AVAILABLE_TOOLS",
]

