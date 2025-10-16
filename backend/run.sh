#!/bin/bash
echo "Starting Skill Assignment Backend..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Start server
echo "Backend running at http://localhost:8000"
echo "API Docs available at http://localhost:8000/docs"
echo ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
