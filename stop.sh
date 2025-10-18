#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping Tolarian Knowledge Base services...${NC}"
echo ""

# Stop backend
if [ -f backend.pid ]; then
    PID=$(cat backend.pid)
    if kill $PID 2>/dev/null; then
        echo -e "${GREEN}✓ Backend API stopped (PID: $PID)${NC}"
    fi
    rm backend.pid
else
    # Try to find and kill by port
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        kill $(lsof -t -i:5000) 2>/dev/null || sudo kill $(sudo lsof -t -i:5000) 2>/dev/null
        echo -e "${GREEN}✓ Backend API stopped${NC}"
    fi
fi

# Stop frontend
if [ -f frontend.pid ]; then
    PID=$(cat frontend.pid)
    if kill $PID 2>/dev/null; then
        echo -e "${GREEN}✓ Frontend stopped (PID: $PID)${NC}"
    fi
    rm frontend.pid
else
    # Try to find and kill by port
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        kill $(lsof -t -i:3000) 2>/dev/null
        echo -e "${GREEN}✓ Frontend stopped${NC}"
    fi
fi

# Ask about database
echo ""
echo -e "${YELLOW}Stop PostgreSQL database? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    docker compose down
    echo -e "${GREEN}✓ PostgreSQL stopped${NC}"
else
    echo -e "${BLUE}ℹ Database is still running${NC}"
fi

echo ""
echo -e "${GREEN}All services stopped!${NC}"
