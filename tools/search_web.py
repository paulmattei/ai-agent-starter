"""
Web search tool using Tavily API.
Provides real-time web search capabilities for the AI agent.
"""

import os
from tavily import TavilyClient
from utils.logging import log_span


def search_web(query: str) -> str:
    """
    Search the web using Tavily API.
    
    Args:
        query (str): The search query
        
    Returns:
        str: Formatted search results with titles, URLs, and content snippets
    
    Examples:
        >>> search_web("latest Python 3.12 features")
        "Search Results for 'latest Python 3.12 features':\n..."
    """
    log_span(f"🔍 Searching web for: {query}", "tool")
    
    try:
        # Get API key
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            error_msg = "TAVILY_API_KEY not found in environment variables"
            log_span(f"✗ {error_msg}", "error")
            return error_msg
        
        # Initialize Tavily client
        client = TavilyClient(api_key=api_key)
        log_span("✓ Tavily client initialized", "tool")
        
        # Perform search
        response = client.search(
            query=query,
            max_results=5,
            include_answer=True,
            include_raw_content=False
        )
        
        # Format results
        result_parts = []
        
        # Add answer if available
        if response.get('answer'):
            result_parts.append(f"Quick Answer:\n{response['answer']}\n")
        
        # Add search results
        if response.get('results'):
            result_parts.append(f"Search Results for '{query}':\n")
            for i, result in enumerate(response['results'], 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No content')
                
                result_parts.append(
                    f"{i}. {title}\n"
                    f"   URL: {url}\n"
                    f"   {content}\n"
                )
        else:
            result_parts.append("No results found.")
        
        formatted_result = "\n".join(result_parts)
        log_span(f"✓ Found {len(response.get('results', []))} results", "tool")
        
        return formatted_result
        
    except Exception as e:
        error_msg = f"Web search failed: {str(e)}"
        log_span(f"✗ {error_msg}", "error")
        return error_msg


