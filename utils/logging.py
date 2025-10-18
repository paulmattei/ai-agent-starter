"""
Logging utilities for the jobbot application.
Provides structured logging that works in both development and production.
"""

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)

# Export configured logger for use across the application
logger = logging.getLogger("jobbot")

