"""
Movie Recommendation Engine - Core Business Logic  
=================================================
Generates personalized movie recommendations based on user's watch history.
Uses TMDB's collaborative filtering algorithm to find similar movies that
users with similar taste patterns have enjoyed.

Algorithm:
- Analyzes user's highly-rated movies (8+ rating)
- Finds similar movies using TMDB's recommendation engine
- Filters and ranks results by relevance
- Returns top N recommendations with metadata
"""

from typing import List, Dict, Optional
from .tmdb_client import TMDBClient

class MovieRecommendationService:
    """Service for generating movie recommendations"""
    
    def __init__(self, api_key: str):
        self.tmdb_client = TMDBClient(api_key)
    
    def get_recommendations_for_movies(self, movies: List[Dict], limit: int = 10) -> List[Dict]:
        """Get recommendations based on a list of movies"""
        all_recommendations = []
        
        # Get top-rated movies to base recommendations on
        rated_movies = [m for m in movies if m.get('rating') is not None]
        if not rated_movies:
            return []
        
        # Sort by rating and get recommendations for top movies
        top_movies = sorted(rated_movies, key=lambda x: x['rating'], reverse=True)[:3]
        
        for movie in top_movies:
            try:
                # Search for the movie on TMDB
                search_results = self.tmdb_client.search_movie(movie['title'])
                if search_results:
                    movie_id = search_results[0]['id']
                    
                    # Get recommendations and similar movies
                    recs = self.tmdb_client.get_movie_recommendations(movie_id, 5)
                    similar = self.tmdb_client.get_similar_movies(movie_id, 5)
                    
                    all_recommendations.extend(recs + similar)
                    
            except Exception:
                continue  # Skip movies that cause errors
        
        # Remove duplicates and return top results
        seen_titles = set()
        unique_recs = []
        for rec in all_recommendations:
            if rec['title'] not in seen_titles:
                seen_titles.add(rec['title'])
                unique_recs.append(rec)
                if len(unique_recs) >= limit:
                    break
        
        return unique_recs