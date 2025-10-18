#!/bin/bash

# Script to set Fly.io secrets from .env file
# Usage: ./scripts/set-fly-secrets.sh [app-name]
#
# This script reads your .env file and sets the secrets in your Fly.io app.
# Saves you from manually copying API keys!

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Show help if requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Set Fly.io secrets from .env file"
    echo ""
    echo "Usage: $0 [app-name]"
    echo ""
    echo "Arguments:"
    echo "  app-name    Optional. Fly.io app name (reads from fly.toml if not provided)"
    echo ""
    echo "Examples:"
    echo "  $0                      # Use app name from fly.toml"
    echo "  $0 my-app-name          # Explicitly specify app name"
    echo ""
    echo "Requirements:"
    echo "  - .env file with OPENAI_API_KEY, E2B_API_KEY, TAVILY_API_KEY"
    echo "  - flyctl installed and authenticated"
    echo "  - fly.toml with app name (if not providing app-name argument)"
    exit 0
fi

# Get app name from argument or fly.toml
APP_NAME="${1:-}"

if [ -z "$APP_NAME" ]; then
    # Try to get app name from fly.toml
    if [ -f "fly.toml" ]; then
        APP_NAME=$(grep -E "^app\s*=" fly.toml | cut -d'"' -f2 | cut -d"'" -f2 | head -1)
    fi
fi

if [ -z "$APP_NAME" ]; then
    echo -e "${RED}Error: Could not determine app name${NC}"
    echo "Usage: $0 [app-name]"
    echo "Or ensure fly.toml exists with app name"
    exit 1
fi

echo -e "${GREEN}Setting secrets for Fly.io app: ${APP_NAME}${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create a .env file with your API keys"
    echo "You can copy env.example: cp env.example .env"
    exit 1
fi

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo -e "${RED}Error: flyctl not found${NC}"
    echo "Please install Fly CLI: https://fly.io/docs/hands-on/install-flyctl/"
    exit 1
fi

# Source the .env file to load variables
echo -e "${YELLOW}Loading secrets from .env...${NC}"
set -a  # Automatically export all variables
source .env
set +a  # Stop auto-exporting

# Check if required variables are set
MISSING_VARS=()

if [ -z "$OPENAI_API_KEY" ]; then
    MISSING_VARS+=("OPENAI_API_KEY")
fi

if [ -z "$E2B_API_KEY" ]; then
    MISSING_VARS+=("E2B_API_KEY")
fi

if [ -z "$TAVILY_API_KEY" ]; then
    MISSING_VARS+=("TAVILY_API_KEY")
fi

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo -e "${RED}Error: Missing required environment variables in .env:${NC}"
    for var in "${MISSING_VARS[@]}"; do
        echo "  - $var"
    done
    exit 1
fi

# Set the secrets in Fly.io
echo -e "${YELLOW}Setting secrets in Fly.io...${NC}"

flyctl secrets set \
    OPENAI_API_KEY="$OPENAI_API_KEY" \
    E2B_API_KEY="$E2B_API_KEY" \
    TAVILY_API_KEY="$TAVILY_API_KEY" \
    --app "$APP_NAME"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Secrets successfully set for app: ${APP_NAME}${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Deploy your app: flyctl deploy"
    echo "  2. Check status: flyctl status --app $APP_NAME"
    echo "  3. View logs: flyctl logs --app $APP_NAME"
else
    echo -e "${RED}✗ Failed to set secrets${NC}"
    exit 1
fi

