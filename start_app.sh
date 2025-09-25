#!/bin/bash
# Horror Movie App Launcher
# Starts both API server and Frontend server

echo "🎬 Starting Horror Movie Recommendation System"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to start API server
start_api() {
    echo "🚀 Starting API Server (FastAPI)..."
    if [ -f "venv/bin/python" ]; then
        ./venv/bin/python app.py
    else
        python3 app.py
    fi
}

# Function to start Frontend server
start_frontend() {
    sleep 3  # Wait for API server to start
    echo "🌐 Starting Frontend Server..."
    python3 serve_frontend.py
}

# Start both servers in the background
echo "Starting servers..."
start_api &
API_PID=$!

start_frontend &
FRONTEND_PID=$!

# Function to handle cleanup when script is terminated
cleanup() {
    echo -e "\n🛑 Shutting down servers..."
    kill $API_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "👋 All servers stopped!"
    exit 0
}

# Set up signal handling for clean shutdown
trap cleanup SIGINT SIGTERM

echo ""
echo "✅ Both servers are starting up!"
echo "🔗 API Server: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for background processes
wait