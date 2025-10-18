#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║           TOLARIAN KNOWLEDGE BASE STARTUP                ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Set environment variables for .NET
export DOTNET_ROOT=$HOME/.dotnet
export PATH="$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools"

# Function to check if Docker is running
check_docker() {
    echo -e "${YELLOW}[1/5] Checking Docker status...${NC}"

    if ! command -v docker &> /dev/null; then
        echo -e "${RED}✗ Docker is not installed. Please install Docker first.${NC}"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        echo -e "${YELLOW}⚠ Docker is not running. Starting Docker service...${NC}"
        sudo service docker start
        sleep 3

        if ! docker info &> /dev/null; then
            echo -e "${RED}✗ Failed to start Docker. Please start it manually.${NC}"
            exit 1
        fi
    fi

    echo -e "${GREEN}✓ Docker is running${NC}"
}

# Function to start PostgreSQL
start_database() {
    echo -e "${YELLOW}[2/5] Starting PostgreSQL database...${NC}"

    # Check if container is already running
    if docker ps --format '{{.Names}}' | grep -q "tolarian_postgres"; then
        echo -e "${GREEN}✓ PostgreSQL is already running${NC}"
    else
        docker compose up -d
        echo -e "${GREEN}✓ PostgreSQL started${NC}"
        echo -e "${YELLOW}  Waiting for database to be ready...${NC}"
        sleep 5
    fi
}

# Function to start backend
start_backend() {
    echo -e "${YELLOW}[3/5] Starting .NET Backend API...${NC}"

    cd DevKnowledgeBase.API || exit 1

    # Kill any existing process on port 5000
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}  Stopping existing backend process...${NC}"
        kill $(lsof -t -i:5000) 2>/dev/null || sudo kill $(sudo lsof -t -i:5000) 2>/dev/null
        sleep 2
    fi

    # Start backend in background
    nohup dotnet run > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../backend.pid

    echo -e "${GREEN}✓ Backend API started (PID: $BACKEND_PID)${NC}"
    echo -e "${YELLOW}  Waiting for API to initialize...${NC}"
    sleep 5

    cd ..
}

# Function to start frontend
start_frontend() {
    echo -e "${YELLOW}[4/5] Starting Next.js Frontend...${NC}"

    cd knowledge-base-ui || exit 1

    # Kill any existing process on port 3000
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}  Stopping existing frontend process...${NC}"
        kill $(lsof -t -i:3000) 2>/dev/null
        sleep 2
    fi

    # Start frontend in background
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../frontend.pid

    echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
    echo -e "${YELLOW}  Waiting for frontend to initialize...${NC}"
    sleep 5

    cd ..
}

# Function to display URLs
show_urls() {
    echo -e "${YELLOW}[5/5] All services started!${NC}"
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    QUICK ACCESS URLS                      ║${NC}"
    echo -e "${GREEN}╠═══════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║${NC}                                                           ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}  ${BLUE}Frontend:${NC}  http://localhost:3000                        ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}  ${BLUE}Backend:${NC}   http://localhost:5000                        ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}  ${BLUE}API Docs:${NC}  http://localhost:5000/openapi/v1.json       ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}  ${BLUE}Database:${NC}  localhost:5432 (tolarian_dev)               ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}                                                           ${GREEN}║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Logs:${NC}"
    echo -e "  Backend:  ${BLUE}tail -f backend.log${NC}"
    echo -e "  Frontend: ${BLUE}tail -f frontend.log${NC}"
    echo ""
    echo -e "${YELLOW}To stop all services:${NC} ${BLUE}./stop.sh${NC} or press ${RED}Ctrl+C${NC}"
    echo ""
}

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down services...${NC}"

    if [ -f backend.pid ]; then
        kill $(cat backend.pid) 2>/dev/null
        rm backend.pid
        echo -e "${GREEN}✓ Backend stopped${NC}"
    fi

    if [ -f frontend.pid ]; then
        kill $(cat frontend.pid) 2>/dev/null
        rm frontend.pid
        echo -e "${GREEN}✓ Frontend stopped${NC}"
    fi

    echo -e "${YELLOW}Database is still running. To stop it, run: ${BLUE}docker compose down${NC}"
    echo -e "${GREEN}Goodbye!${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Main execution
check_docker
start_database
start_backend
start_frontend
show_urls

# Keep script running
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait indefinitely
while true; do
    sleep 1
done
