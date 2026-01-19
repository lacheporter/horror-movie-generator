# NightReel API Backend

A clean, mobile-ready FastAPI backend for horror movie recommendations with machine learning-based rating predictions. **NightReel** - your personal horror movie discovery engine, designed specifically for iOS app consumption.

## 🏗️ Project Structure

```
nightreel/
├── 📁 api/                     # FastAPI routes & models
│   ├── models/
│   │   └── movie_models.py     # Pydantic request/response models
│   └── routes/
│       └── movies.py           # Movie API endpoints
├── 📁 core/                    # Business logic & services
│   ├── tmdb_client.py          # TMDB API integration
│   ├── recommendation_service.py # Movie recommendation engine
│   ├── prediction_service.py   # ML rating predictions
│   └── supabase_service.py     # Database integration (optional)
├── 📁 data/                    # Data management
│   └── movie_data.py           # Sample movie data
├── app.py                      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── schema.sql                  # Database schema (optional)
├── setup_supabase.py           # Database setup script (optional)
├── .env                        # API keys & configuration
└── Makefile                    # Build commands
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

### 🔌 Mobile-Ready API
- RESTful endpoints optimized for iOS consumption
- FastAPI with automatic OpenAPI documentation
- CORS enabled for mobile app integration
- Health checks and error handling

### 🗄️ Database Options
- Static sample data (default)
- Optional Supabase PostgreSQL integration
- Migration scripts included

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.13.7
- Virtual environment (recommended)
- TMDB API key

### Installation
```bash
# Clone the repository
cd /path/to/nightreel

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

#### Quick Setup (First Time)
```bash
# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

#### Quick Start
```bash
# Activate virtual environment
source venv/bin/activate

# Start the API server
python app.py
# Server runs at http://localhost:8000
```

#### Alternative Commands
```bash
# Using FastAPI directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Using Make commands
make run        # Start server
make test       # Test endpoints
make clean      # Clean cache files
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

### Mobile-Optimized Endpoints
- `GET /health/mobile` - Mobile app health check
- `GET /api/movies/moods` - Available movie moods
- `GET /api/movies/spin?mood=creepy` - Get random movie by mood
- `GET /api/movies/recommendations` - Personalized recommendations
- `GET /api/movies/predictions` - Rating predictions
- `GET /api/movies/stats` - User statistics

### Response Models
- `Movie` - Movie data with ratings and metadata
- `MovieRecommendation` - Recommended movie with similarity score
- `RatingPrediction` - ML-predicted rating with confidence
- `UserStats` - User preferences and viewing statistics

## 🧪 Testing

```bash
# Test API health
curl http://localhost:8000/health

# Test mobile endpoints
curl http://localhost:8000/health/mobile
curl "http://localhost:8000/api/movies/moods"
curl "http://localhost:8000/api/movies/spin?mood=creepy"

# View API documentation
open http://localhost:8000/docs
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

### Swift iOS Integration
```swift
// APIService.swift - Example integration
struct APIService {
    static let baseURL = "http://localhost:8000"
    
    static func getMovieMoods() async throws -> [String] {
        let url = URL(string: "\(baseURL)/api/movies/moods")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode([String].self, from: data)
    }
    
    static func spinMovie(mood: String) async throws -> Movie {
        let url = URL(string: "\(baseURL)/api/movies/spin?mood=\(mood)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(Movie.self, from: data)
    }
}
```

## �️ Optional Database Setup

By default, the API uses sample data. For persistent storage:

```bash
# Set up Supabase (optional)
python setup_supabase.py

# Update .env with your Supabase credentials
SUPABASE_URL=your_project_url
SUPABASE_ANON_KEY=your_anon_key
```

## 🏃‍♂️ Quick Start

1. **Activate environment**: `source venv/bin/activate`
2. **Start the API server**: `python app.py`
3. **Test the API**: `curl http://localhost:8000/health/mobile`
4. **View API docs**: Open `http://localhost:8000/docs` in browser
5. **Build your iOS app**: Use the Swift examples above

## 🚀 Next Steps for iOS Development

1. **Create Xcode project** with provided Swift code examples
2. **Deploy backend** to Railway, Render, or similar service
3. **Update API base URL** in iOS app to production endpoint
4. **Optional**: Set up Supabase for user data persistence

## 🎯 Future Backend Enhancements

- [ ] User authentication with JWT tokens
- [ ] Rate limiting and API security
- [ ] Enhanced ML recommendation models
- [ ] Caching layer for better performance
- [ ] Docker containerization
- [ ] CI/CD pipeline setup

---

**NightReel provides a clean, mobile-ready API foundation for your iOS horror movie discovery app.**