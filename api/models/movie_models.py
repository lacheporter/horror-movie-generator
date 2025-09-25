"""
API Data Models - Pydantic Schemas
===================================
Defines data structures for API requests and responses using Pydantic models.
Provides type validation, serialization, and automatic API documentation.

Models:
- Movie: Basic movie information with optional rating
- MovieRecommendation: Recommended movie with similarity scoring
- RatingPrediction: AI-predicted rating with confidence level  
- UserStats: User preferences and watching statistics
"""

from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
    """Movie data model"""
    title: str
    year: str
    rating: Optional[float] = None
    genres: List[str] = []
    overview: str = ""
    vote_average: float = 0
    poster_path: Optional[str] = None

class MovieRecommendation(BaseModel):
    """Movie recommendation response model"""
    title: str
    year: str
    genres: List[str]
    overview: str
    vote_average: float
    popularity: float
    poster_path: Optional[str] = None
    similarity_score: Optional[float] = None

class RatingPrediction(BaseModel):
    """Rating prediction response model"""
    title: str
    year: str
    predicted_rating: float
    confidence: float
    actual_tmdb_rating: float
    genres: List[str]

class UserStats(BaseModel):
    """User statistics model"""
    total_movies: int
    rated_movies: int
    unrated_movies: int
    average_rating: float
    top_genres: List[dict]

class APIResponse(BaseModel):
    """Generic API response wrapper"""
    success: bool
    message: str
    data: Optional[dict] = None