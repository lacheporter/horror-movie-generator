"""
Movie Data Store - Centralized Data Management
==============================================
Manages all movie data and user preferences in a centralized location.
In production, this would typically be replaced with database models.

Features:
- Sample movie database with ratings and metadata
- User statistics calculation (average rating, genre preferences)  
- Separation of rated vs unrated movies
- Legacy format conversion for backward compatibility

Contains: Horror/thriller movies with mix of rated and unrated entries
"""

from typing import List, Dict

# Sample movie data (in a real app, this might come from a database)
WATCHED_MOVIES_DATA = [
    {
        "title": "Copycat",
        "year": "1995", 
        "rating": 8.0,
        "genres": ["Horror", "Thriller", "Crime"],
        "overview": "A psychological thriller about a serial killer copycat.",
        "vote_average": 6.6,
        "poster_path": None
    },
    {
        "title": "Seven",
        "year": "1995",
        "rating": 9.0, 
        "genres": ["Horror", "Thriller", "Crime"],
        "overview": "Two detectives hunt a serial killer who uses the seven deadly sins.",
        "vote_average": 8.6,
        "poster_path": None
    },
    {
        "title": "The Wailing",
        "year": "2016",
        "rating": 9.0,
        "genres": ["Horror", "Mystery", "Thriller"],
        "overview": "A mysterious illness spreads in a remote Korean village.",
        "vote_average": 7.5,
        "poster_path": None
    },
    {
        "title": "IT",
        "year": "2017",
        "rating": 8.0,
        "genres": ["Horror", "Thriller"],
        "overview": "A group of kids face their fears against the evil clown Pennywise.",
        "vote_average": 7.3,
        "poster_path": None
    },
    {
        "title": "Hereditary", 
        "year": "2018",
        "rating": 8.0,
        "genres": ["Horror", "Drama", "Mystery"],
        "overview": "A family haunted by tragedy is haunted by something far worse.",
        "vote_average": 7.3,
        "poster_path": None
    },
    {
        "title": "Smile",
        "year": "2022",
        "rating": 7.2,
        "genres": ["Horror", "Mystery", "Thriller"],
        "overview": "After witnessing a bizarre, traumatic incident, Dr. Rose Cotter starts experiencing frightening occurrences.",
        "vote_average": 6.5,
        "poster_path": None
    },
    {
        "title": "Together",
        "year": "2021",
        "rating": None,  # Will be predicted
        "genres": ["Horror", "Drama"],
        "overview": "A pandemic horror story.",
        "vote_average": 6.2,
        "poster_path": None
    },
    {
        "title": "The Platform 2", 
        "year": "2024",
        "rating": None,  # Will be predicted
        "genres": ["Horror", "Sci-Fi", "Thriller"],
        "overview": "Sequel to the dystopian thriller.",
        "vote_average": 5.8,
        "poster_path": None
    },
    {
        "title": "Cobweb",
        "year": "2023", 
        "rating": None,  # Will be predicted
        "genres": ["Horror", "Mystery"],
        "overview": "A young boy hears mysterious sounds from within the walls.",
        "vote_average": 6.1,
        "poster_path": None
    }
]

def get_default_watched_movies():
    """Get the default watched movies data in the format expected by the legacy system"""
    # Convert to the format expected by MovieRecommendationSystem
    legacy_format = []
    for movie in WATCHED_MOVIES_DATA:
        if movie['rating'] is not None:
            legacy_format.append((movie['title'], movie['year'], movie['rating']))
        else:
            legacy_format.append((movie['title'], movie['year']))
    return legacy_format

class MovieDataService:
    """Service for managing movie data"""
    
    @staticmethod
    def get_all_movies() -> List[Dict]:
        """Get all movies"""
        return WATCHED_MOVIES_DATA.copy()
    
    @staticmethod
    def get_rated_movies() -> List[Dict]:
        """Get only rated movies"""
        return [movie for movie in WATCHED_MOVIES_DATA if movie['rating'] is not None]
    
    @staticmethod
    def get_unrated_movies() -> List[Dict]:
        """Get only unrated movies"""
        return [movie for movie in WATCHED_MOVIES_DATA if movie['rating'] is None]
    
    @staticmethod
    def get_user_stats() -> Dict:
        """Calculate user statistics"""
        all_movies = MovieDataService.get_all_movies()
        rated_movies = MovieDataService.get_rated_movies()
        unrated_movies = MovieDataService.get_unrated_movies()
        
        if rated_movies:
            avg_rating = sum(m['rating'] for m in rated_movies) / len(rated_movies)
            
            # Count genres
            genre_counts = {}
            for movie in rated_movies:
                for genre in movie['genres']:
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
            top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        else:
            avg_rating = 0
            top_genres = []
        
        return {
            "total_movies": len(all_movies),
            "rated_movies": len(rated_movies),
            "unrated_movies": len(unrated_movies),
            "average_rating": round(avg_rating, 1),
            "top_genres": [{"genre": g[0], "count": g[1]} for g in top_genres]
        }