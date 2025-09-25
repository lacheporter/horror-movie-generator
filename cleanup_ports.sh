#!/bin/bash
# Port Cleanup Script - Kill processes on horror movie app ports

echo "🧹 Cleaning up Horror Movie App ports..."

# Function to kill process on a specific port
kill_port() {
    local port=$1
    local pids=$(lsof -t -i:$port 2>/dev/null)
    
    if [ -n "$pids" ]; then
        echo "🔪 Killing processes on port $port: $pids"
        echo "$pids" | xargs kill -9 2>/dev/null
        sleep 1
        
        # Check if processes are still running
        local remaining=$(lsof -t -i:$port 2>/dev/null)
        if [ -z "$remaining" ]; then
            echo "✅ Port $port is now free"
        else
            echo "⚠️  Some processes on port $port may still be running"
        fi
    else
        echo "✅ Port $port is already free"
    fi
}

# Clean up both ports
kill_port 8000  # API server
kill_port 3000  # Frontend server

echo ""
echo "🎬 Port cleanup complete!"
echo "You can now start your servers:"
echo "  ./venv/bin/python app.py"
echo "  ./venv/bin/python serve_frontend.py"