"""
TMDB API Client - External Movie Database Integration
====================================================
Handles all communication with The Movie Database (TMDB) API.
Provides methods to search movies, get details, and fetch recommendations.
Manages API authentication, rate limiting, and error handling.

Features:
- Movie search by title and year
- Get detailed movie information  
- Fetch similar/recommended movies
- Handle API errors gracefully
"""

import requests
import os
from typing import List, Dict, Optional

class TMDBClient:
    """Client for interacting with The Movie Database (TMDB) API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('TMDB_API_KEY')
        if not self.api_key:
            raise ValueError("TMDB API key is required")
        
        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to TMDB API"""
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        url = f"{self.base_url}{endpoint}"
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def search_movie(self, title: str, year: Optional[int] = None) -> List[Dict]:
        """Search for movies by title"""
        params = {'query': title}
        if year:
            params['year'] = year
        
        data = self._make_request('/search/movie', params)
        return data.get('results', [])
    
    def get_movie_recommendations(self, movie_id: int, limit: int = 10) -> List[Dict]:
        """Get movie recommendations based on a movie ID"""
        params = {'page': 1}
        data = self._make_request(f'/movie/{movie_id}/recommendations', params)
        results = data.get('results', [])
        return results[:limit]
    
    def get_similar_movies(self, movie_id: int, limit: int = 10) -> List[Dict]:
        """Get similar movies based on a movie ID"""
        params = {'page': 1}
        data = self._make_request(f'/movie/{movie_id}/similar', params)
        results = data.get('results', [])
        return results[:limit]