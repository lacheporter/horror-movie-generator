#!/usr/bin/env python3
"""
Frontend Server - Simple HTTP Server for Horror Movie UI
========================================================
Serves the HTML frontend on http://localhost:3000
Run this alongside your FastAPI server (app.py) to have a complete system.

Usage: python serve_frontend.py
"""

import http.server
import socketserver
import os
import signal
import sys

PORT = 3000
FRONTEND_DIR = "frontend"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow API calls to localhost:8000
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    def signal_handler(sig, frame):
        print('\n🛑 Shutting down frontend server...')
        sys.exit(0)
    
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    # Change to project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Check if frontend directory exists
    if not os.path.exists(FRONTEND_DIR):
        print(f"❌ Frontend directory '{FRONTEND_DIR}' not found!")
        return
    
    # Configure server to reuse address (prevents "Address already in use" errors)
    class ReuseAddrTCPServer(socketserver.TCPServer):
        allow_reuse_address = True
    
    # Start the server
    try:
        with ReuseAddrTCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print("🌐 Horror Movie Frontend Server")
            print("=" * 40)
            print(f"🚀 Server running at: http://localhost:{PORT}")
            print(f"📁 Serving files from: {FRONTEND_DIR}/")
            print("")
            print("💡 Make sure your API server is also running:")
            print("   ./venv/bin/python app.py")
            print("")
            print("🛑 Press Ctrl+C to stop the server")
            
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print("💡 Try: lsof -i :3000 to see what's using the port")
            print("💡 Or: kill $(lsof -t -i:3000) to stop it")
        else:
            print(f"❌ Server error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()