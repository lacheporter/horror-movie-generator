#!/bin/bash
# Standard Python Project Setup Script

echo "🎬 Setting up Horror Movie Recommendation System"
echo "================================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment and install dependencies
echo "⬇️  Installing dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    echo "# Get your TMDB API key from https://www.themoviedb.org/settings/api" > .env
    echo "TMDB_API_KEY=your_api_key_here" >> .env
    echo "📝 Please update .env with your actual TMDB API key"
fi

# Run tests to verify setup
echo "🧪 Testing installation..."
./venv/bin/python test_structure.py

echo ""
echo "✅ Setup complete! You can now run:"
echo "   make help          # See all available commands"
echo "   make dev           # Start the full application"
echo "   make run-cli       # Start CLI interface"
echo "   ./venv/bin/python app.py  # Start API server only"