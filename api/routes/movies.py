
#Defines REST API endpoints for movie-related operations:


from fastapi import APIRouter, HTTPException
from typing import List
import os

from api.models.movie_models import Movie, MovieRecommendation, RatingPrediction, UserStats
from core.recommendation_service import MovieRecommendationService
from core.prediction_service import RatingPredictionService
from data.movie_data import MovieDataService

router = APIRouter(prefix="/api/movies", tags=["movies"])

@router.post("/rate/{movie_title}")
async def rate_movie(movie_title: str, rating: float):
    """Rate a movie (1-10 scale)"""
    if not 1 <= rating <= 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
    
    try:
        success = MovieDataService.rate_movie(movie_title, rating)
        if not success:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return {"message": f"Movie '{movie_title}' rated {rating}/10 successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rate movie: {str(e)}")

@router.delete("/rate/{movie_title}")
async def remove_rating(movie_title: str):
    """Remove rating from a movie"""
    try:
        success = MovieDataService.remove_rating(movie_title)
        if not success:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return {"message": f"Rating removed from '{movie_title}' successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove rating: {str(e)}")

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

@router.get("/random-roulette", response_model=List[MovieRecommendation])
async def get_random_horror_movies(limit: int = 10):
    """Get random horror movies that you haven't watched yet - Horror Roulette style!"""
    api_key = os.getenv('TMDB_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="TMDB API key not configured")
    
    try:
        # Get user's watched movies to exclude them
        watched_movies = MovieDataService.get_all_movies()
        watched_titles = {movie['title'].lower().strip() for movie in watched_movies}
        
        recommendation_service = MovieRecommendationService(api_key)
        random_movies = recommendation_service.get_random_horror_movies(watched_titles, limit)
        
        # Convert to response model
        result = []
        for movie in random_movies:
            movie_rec = MovieRecommendation(
                title=movie['title'],
                year=movie.get('release_date', '')[:4] if movie.get('release_date') else '',
                genres=movie.get('genre_names', ['Horror']),
                overview=movie.get('overview', ''),
                vote_average=movie.get('vote_average', 0),
                popularity=movie.get('popularity', 0),
                poster_path=movie.get('poster_path')
            )
            result.append(movie_rec)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get random movies: {str(e)}")

@router.get("/featured-recommendation", response_model=MovieRecommendation)
async def get_featured_recommendation():
    """Get a single featured movie recommendation for the homepage"""
    api_key = os.getenv('TMDB_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="TMDB API key not configured")
    
    try:
        # Get user's watched movies to exclude them
        watched_movies = MovieDataService.get_all_movies()
        watched_titles = {movie['title'].lower().strip() for movie in watched_movies}
        
        recommendation_service = MovieRecommendationService(api_key)
        
        # Try to get a recommendation based on user's ratings first
        if watched_movies:
            recommendations = recommendation_service.get_recommendations_for_movies(watched_movies, 1)
            if recommendations:
                movie = recommendations[0]
                # Convert to response model
                movie_rec = MovieRecommendation(
                    title=movie['title'],
                    year=movie.get('release_date', '')[:4] if movie.get('release_date') else '',
                    genres=movie.get('genre_names', ['Horror']),
                    overview=movie.get('overview', ''),
                    vote_average=movie.get('vote_average', 0),
                    popularity=movie.get('popularity', 0),
                    poster_path=movie.get('poster_path')
                )
                return movie_rec
        
        # Fallback to random horror movie if no personalized recommendations
        random_movies = recommendation_service.get_random_horror_movies(watched_titles, 1)
        if random_movies:
            movie = random_movies[0]
            movie_rec = MovieRecommendation(
                title=movie['title'],
                year=movie.get('release_date', '')[:4] if movie.get('release_date') else '',
                genres=movie.get('genre_names', ['Horror']),
                overview=movie.get('overview', ''),
                vote_average=movie.get('vote_average', 0),
                popularity=movie.get('popularity', 0),
                poster_path=movie.get('poster_path')
            )
            return movie_rec
        
        raise HTTPException(status_code=404, detail="No movies found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get featured recommendation: {str(e)}")

@router.get("/spin-roulette/{mood}", response_model=MovieRecommendation)
async def spin_for_mood_movie(mood: str):
    """Spin the roulette for a single movie based on emotional mood"""
    api_key = os.getenv('TMDB_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="TMDB API key not configured")
    
    # Validate mood
    valid_moods = ['gory', 'creepy', 'mysterious', 'jumpscare', 'body-horror', 'paranoid']
    if mood.lower() not in valid_moods:
        raise HTTPException(status_code=400, detail=f"Invalid mood. Must be one of: {', '.join(valid_moods)}")
    
    try:
        # Get user's watched movies to exclude them
        watched_movies = MovieDataService.get_all_movies()
        watched_titles = {movie['title'].lower().strip() for movie in watched_movies}
        
        recommendation_service = MovieRecommendationService(api_key)
        movie = recommendation_service.spin_for_mood_movie(mood.lower(), watched_titles)
        
        if not movie:
            raise HTTPException(status_code=404, detail=f"No unwatched {mood} movies found")
        
        # Convert to response model
        movie_rec = MovieRecommendation(
            title=movie['title'],
            year=movie.get('release_date', '')[:4] if movie.get('release_date') else '',
            genres=movie.get('genre_names', ['Horror']),
            overview=movie.get('overview', ''),
            vote_average=movie.get('vote_average', 0),
            popularity=movie.get('popularity', 0),
            poster_path=movie.get('poster_path')
        )
        
        return movie_rec
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to spin for {mood} movie: {str(e)}")

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
    """Get movies filtered by horror category: gory, creepy, mysterious, jumpscare, body-horror, paranoid"""
    valid_categories = ['gory', 'creepy', 'mysterious', 'jumpscare', 'body-horror', 'paranoid']
    
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
        'jumpscare': 'Sudden scares and paranormal frights',
        'body-horror': 'Physical transformation and grotesque imagery',
        'paranoid': 'Conspiracy, surveillance, and psychological thriller'
    }
    return descriptions.get(category.lower(), 'Unknown category')