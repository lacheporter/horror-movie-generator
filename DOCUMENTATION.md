# 📝 Project File Documentation

## 🗂️ Complete File Structure with Descriptions

```
horror-movie-generator/
├── 🚀 app.py                           # Main FastAPI server entry point
├── 🧪 test_structure.py                # Project validation and integration tests
│
├── 📁 api/                             # HTTP Interface Layer
│   ├── __init__.py                     # API package initialization
│   ├── models/                         # Request/Response Schemas
│   │   ├── __init__.py                 # Models package initialization  
│   │   └── movie_models.py             # Pydantic data models for API
│   └── routes/                         # HTTP Endpoint Definitions
│       ├── __init__.py                 # Routes package initialization
│       └── movies.py                   # Movie-related API endpoints
│
├── 📁 core/                            # Business Logic Layer  
│   ├── __init__.py                     # Core services package initialization
│   ├── tmdb_client.py                  # External Movie Database integration
│   ├── recommendation_service.py       # Movie recommendation engine
│   └── prediction_service.py           # AI rating prediction algorithms
│
├── 📁 data/                            # Data Management Layer
│   ├── __init__.py                     # Data layer package initialization
│   └── movie_data.py                   # Centralized data store and statistics
│
└── 📁 cli/                             # Command Line Interface
    ├── __init__.py                     # CLI package initialization
    └── main.py                         # Interactive terminal application
```

## 🎯 File Purposes

### **Entry Points**
- **`app.py`** - Start FastAPI server for mobile app API
- **`cli/main.py`** - Run interactive terminal interface
- **`test_structure.py`** - Validate project structure works

### **API Layer** (`api/`)
- **Handles HTTP requests/responses**
- **Converts between API and business logic**  
- **Provides type-safe JSON endpoints**

### **Core Layer** (`core/`)
- **Contains all business logic**
- **Independent of HTTP/CLI interfaces**
- **Handles recommendations and predictions**

### **Data Layer** (`data/`)
- **Manages all data operations**
- **Provides statistics and analysis**
- **Future: Database integration**

### **CLI Layer** (`cli/`)
- **Simple terminal user interface**
- **3-option menu system**
- **Direct user interaction**

## 🔧 How Files Work Together

```
CLI App → Core Services → Data Layer → TMDB API
   ↓            ↑
API Server → API Routes → API Models
```

1. **User interfaces** (CLI/API) call **core services**
2. **Core services** process business logic and call **data layer**  
3. **Data layer** manages information and external APIs
4. **Results flow back** through the same layers

## 📚 Key Documentation Features

✅ **Every file has a purpose statement**  
✅ **Algorithm explanations where relevant**  
✅ **Usage instructions for entry points**  
✅ **Architecture diagrams in comments**  
✅ **Feature lists for complex modules**

This structure makes the codebase **self-documenting** and easy to understand for new developers! 🎬