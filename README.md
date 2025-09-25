# Movie Recommendation System - Organized Structure

A comprehensive movie recommendation system with machine learning-based rating predictions, built with FastAPI for mobile app development.

## 🏗️ Project Structure

```
horror-movie-generator/
├── 📁 api/                     # API layer
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── movie_models.py     # Pydantic models for API requests/responses
│   └── routes/
│       ├── __init__.py
│       └── movies.py           # Movie-related API endpoints
├── 📁 core/                    # Core business logic
│   ├── __init__.py
│   ├── tmdb_client.py          # TMDB API client wrapper
│   ├── recommendation_service.py # Movie recommendation engine
│   └── prediction_service.py   # Rating prediction algorithms
├── 📁 data/                    # Data management
│   ├── __init__.py
│   └── movie_data.py           # Centralized movie data and statistics
├── 📁 cli/                     # Command line interface
│   ├── __init__.py
│   └── main.py                 # Simple 3-option CLI app
├── 📁 tests/                   # Test files
│   └── __init__.py
├── 📁 src/                     # Legacy code (being phased out)
├── app.py                      # Main FastAPI application
├── test_structure.py           # Test script for new organization
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Features

### 🎬 Movie Recommendations
- Content-based filtering using TMDB API
- Genre preference analysis
- Similar movie discovery

### 🔮 Rating Predictions
- Machine learning-based predictions for unrated movies
- Genre-based similarity analysis
- Confidence scoring

### 🔌 API Endpoints
- RESTful API for mobile app integration
- FastAPI with automatic documentation
- CORS enabled for cross-origin requests

### 💻 CLI Interface
- Simple 3-option menu (Recommendations, Predictions, Exit)
- User-friendly terminal interface
- Streamlined movie management

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.13.7
- Virtual environment (recommended)
- TMDB API key

### Installation
```bash
# Clone the repository
cd /path/to/horror-movie-generator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "TMDB_API_KEY=your_api_key_here" > .env
```

### Running the Applications

#### FastAPI Server
```bash
# Start the API server
python app.py

# Access the API
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

#### CLI Application
```bash
# Run the command line interface
python cli/main.py
```

## 📚 API Documentation

### Endpoints

#### Health Check
- `GET /` - Root endpoint
- `GET /health` - API health status

#### Movies
- `GET /api/movies/watched` - Get watched movies list
- `GET /api/movies/recommendations?limit=10` - Get movie recommendations
- `GET /api/movies/predictions` - Get rating predictions for unrated movies
- `GET /api/movies/stats` - Get user statistics and preferences

### Response Models
All API responses use Pydantic models for type safety:
- `Movie` - Individual movie with rating and metadata
- `MovieRecommendation` - Recommended movie with similarity score
- `RatingPrediction` - Predicted rating with confidence level
- `UserStats` - User preferences and statistics

## 🧪 Testing

### Test the Structure
```bash
# Test all imports and basic functionality
python test_structure.py
```

### Test Individual Components
```bash
# Test API endpoints
curl -X GET "http://localhost:8000/api/movies/watched"
curl -X GET "http://localhost:8000/api/movies/predictions"

# Test CLI (interactive)
python cli/main.py
```

## 🔧 Architecture

### Separation of Concerns
- **API Layer** (`api/`): HTTP endpoints and request/response handling
- **Core Layer** (`core/`): Business logic and external service integration
- **Data Layer** (`data/`): Data models and centralized data management

### Key Design Decisions
1. **Modular Architecture**: Each component has a single responsibility
2. **Dependency Injection**: Services receive dependencies as parameters
3. **Type Safety**: Pydantic models for all data structures
4. **Error Handling**: Comprehensive exception handling with user-friendly messages
5. **API-First**: Designed primarily for mobile app consumption

### External Dependencies
- **TMDB API**: Movie data and metadata
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **scikit-learn**: Machine learning algorithms (in legacy code)

## 🚀 Mobile App Ready

This backend is specifically designed for mobile app development:

### API Features
- **RESTful endpoints** for all functionality
- **JSON responses** with consistent structure
- **CORS enabled** for cross-platform requests
- **Automatic documentation** at `/docs`
- **Error handling** with appropriate HTTP status codes

### Recommended Mobile Integration
```javascript
// Example mobile app integration
const API_BASE = 'http://your-server:8000/api/movies';

// Get recommendations
fetch(`${API_BASE}/recommendations?limit=10`)
  .then(response => response.json())
  .then(movies => displayRecommendations(movies));

// Get rating predictions
fetch(`${API_BASE}/predictions`)
  .then(response => response.json())
  .then(predictions => showPredictions(predictions));
```

## 🔄 Migration from Legacy Code

The original monolithic files are being gradually replaced:
- ✅ `main.py` → `cli/main.py` (Simplified 3-option interface)
- ✅ `src/movie_recommender.py` → `core/recommendation_service.py`
- ✅ `src/rating_predictor.py` → `core/prediction_service.py`
- ✅ Hardcoded data → `data/movie_data.py`
- ✅ `app_simple.py` → `app.py` (Organized with proper routing)

## 🏃‍♂️ Quick Start

1. **Start the API server**: `python app.py`
2. **Test in another terminal**: `curl http://localhost:8000/health`
3. **Try the CLI**: `python cli/main.py`
4. **View API docs**: Open `http://localhost:8000/docs` in browser

## 🎯 Future Enhancements

- [ ] Database integration (replace static data)
- [ ] User authentication and personalized watchlists
- [ ] More sophisticated ML models
- [ ] Caching layer for better performance
- [ ] Containerization with Docker
- [ ] Production deployment configuration

---

**Note**: This organized structure provides a scalable foundation for mobile app development while maintaining the simplicity of the original CLI application.