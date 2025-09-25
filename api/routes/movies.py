"""
API Routes - Movie Endpoints
=============================
Defines REST API endpoints for movie-related operations:
- GET /api/movies/watched - List of watched movies
- GET /api/movies/recommendations - Get movie recommendations  
- GET /api/movies/predictions - Get rating predictions
- GET /api/movies/stats - User statistics and preferences

All endpoints return JSON responses using Pydantic models for type safety.
"""

from fastapi import APIRouter, HTTPException
from typing import List
import os

from api.models.movie_models import Movie, MovieRecommendation, RatingPrediction, UserStats
from core.recommendation_service import MovieRecommendationService
from core.prediction_service import RatingPredictionService
from data.movie_data import MovieDataService

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.get("/watched", response_model=List[Movie])
async def get_watched_movies():
    """Get list of all watched movies"""
    movies = MovieDataService.get_all_movies()
    return [Movie(**movie) for movie in movies]

@router.get("/recommendations", response_model=List[MovieRecommendation])
async def get_recommendations(limit: int = 10):
    """Get movie recommendations"""
    api_key = os.getenv('TMDB_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="TMDB API key not configured")
    
    try:
        movies = MovieDataService.get_all_movies()
        recommendation_service = MovieRecommendationService(api_key)
        recommendations = recommendation_service.get_recommendations_for_movies(movies, limit)
        
        # Convert to response model
        result = []
        for rec in recommendations:
            movie_rec = MovieRecommendation(
                title=rec['title'],
                year=rec.get('release_date', '')[:4] if rec.get('release_date') else '',
                genres=rec.get('genre_names', ['Unknown']),  # Would need genre lookup
                overview=rec.get('overview', ''),
                vote_average=rec.get('vote_average', 0),
                popularity=rec.get('popularity', 0),
                poster_path=rec.get('poster_path')
            )
            result.append(movie_rec)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.get("/predictions", response_model=List[RatingPrediction])
async def get_rating_predictions():
    """Get rating predictions for unrated movies"""
    try:
        movies = MovieDataService.get_all_movies()
        prediction_service = RatingPredictionService()
        predictions = prediction_service.get_predictions_for_unrated_movies(movies)
        
        return [RatingPrediction(**pred) for pred in predictions]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/stats", response_model=UserStats)
async def get_user_stats():
    """Get user statistics and preferences"""
    try:
        stats = MovieDataService.get_user_stats()
        return UserStats(**stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")