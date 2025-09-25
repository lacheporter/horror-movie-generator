
#Defines REST API endpoints for movie-related operations:


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

@router.get("/by-category/{category}", response_model=List[Movie])
async def get_movies_by_horror_category(category: str):
    """Get movies filtered by horror category: gory, creepy, mysterious, jumpscare"""
    valid_categories = ['gory', 'creepy', 'mysterious', 'jumpscare']
    
    if category.lower() not in valid_categories:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        )
    
    try:
        all_movies = MovieDataService.get_all_movies()
        filtered_movies = [
            movie for movie in all_movies 
            if movie.get('horror_category', '').lower() == category.lower()
        ]
        
        return [Movie(**movie) for movie in filtered_movies]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get movies by category: {str(e)}")

@router.get("/categories")
async def get_horror_categories():
    """Get available horror categories with movie counts"""
    try:
        all_movies = MovieDataService.get_all_movies()
        
        category_counts = {}
        for movie in all_movies:
            category = movie.get('horror_category', 'unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        categories = [
            {"name": category, "count": count, "description": _get_category_description(category)}
            for category, count in category_counts.items()
            if category != 'unknown'
        ]
        
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories: {str(e)}")

def _get_category_description(category: str) -> str:
    """Get description for horror categories"""
    descriptions = {
        'gory': 'Blood, violence, and brutal visuals',
        'creepy': 'Psychologically unsettling and disturbing',
        'mysterious': 'Puzzles, investigations, and hidden secrets',
        'jumpscare': 'Sudden scares and paranormal frights'
    }
    return descriptions.get(category.lower(), 'Unknown category')