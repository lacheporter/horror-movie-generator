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
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed movie information by ID"""
        return self._make_request(f'/movie/{movie_id}')
    
    def get_movie_poster_path(self, title: str, year: Optional[str] = None) -> Optional[str]:
        """Get poster path for a movie by searching title and year"""
        try:
            year_int = int(year) if year and year.isdigit() else None
            results = self.search_movie(title, year_int)
            
            if results:
                # Return the poster path of the first (best) match
                return results[0].get('poster_path')
            return None
        except Exception as e:
            print(f"Error fetching poster for '{title}': {e}")
            return None
    
    def discover_movies(self, with_genres: List[int] = None, page: int = 1, 
                       sort_by: str = 'popularity.desc', vote_average_gte: float = None,
                       vote_count_gte: int = None) -> List[Dict]:
        """Discover movies using various filters"""
        params = {
            'page': page,
            'sort_by': sort_by
        }
        
        if with_genres:
            params['with_genres'] = ','.join(map(str, with_genres))
        if vote_average_gte is not None:
            params['vote_average.gte'] = vote_average_gte
        if vote_count_gte is not None:
            params['vote_count.gte'] = vote_count_gte
        
        data = self._make_request('/discover/movie', params)
        return data.get('results', [])