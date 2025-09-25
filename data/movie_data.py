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

# Sample movie data with horror experience categories
WATCHED_MOVIES_DATA = [
    {
        "title": "Copycat",
        "year": "1995", 
        "rating": 8.0,
        "genres": ["Horror", "Thriller", "Crime"],
        "horror_category": "creepy",  # Psychological thriller
        "intensity_level": 3,
        "overview": "A psychological thriller about a serial killer copycat.",
        "vote_average": 6.6,
        "poster_path": "/oMgwJb016znNZcpDR20eXxZoW8A.jpg"
    },
    {
        "title": "Seven",
        "year": "1995",
        "rating": 9.0, 
        "genres": ["Horror", "Thriller", "Crime"],
        "horror_category": "mysterious",  # Investigation-based horror
        "intensity_level": 4,
        "overview": "Two detectives hunt a serial killer who uses the seven deadly sins.",
        "vote_average": 8.6,
        "poster_path": "/f7CPfYN2bxr43Cr4fCYWjUKoVEs.jpg"
    },
    {
        "title": "The Wailing",
        "year": "2016",
        "rating": 9.0,
        "genres": ["Horror", "Mystery", "Thriller"],
        "horror_category": "mysterious",  # Occult mystery
        "intensity_level": 4,
        "overview": "A mysterious illness spreads in a remote Korean village.",
        "vote_average": 7.5,
        "poster_path": "/aXlL7yYwpXInhltamtzKQFBG08G.jpg"
    },
    {
        "title": "IT",
        "year": "2017",
        "rating": 8.0,
        "genres": ["Horror", "Thriller"],
        "horror_category": "jumpscare",  # Classic jump scares
        "intensity_level": 3,
        "overview": "A group of kids face their fears against the evil clown Pennywise.",
        "vote_average": 7.3,
        "poster_path": "/9E2y5Q7WlCVNEhP5GiVTjhEhx1o.jpg"
    },
    {
        "title": "Hereditary", 
        "year": "2018",
        "rating": 8.0,
        "genres": ["Horror", "Drama", "Mystery"],
        "horror_category": "creepy",  # Deeply unsettling
        "intensity_level": 5,
        "overview": "A family haunted by tragedy is haunted by something far worse.",
        "vote_average": 7.3,
        "poster_path": "/4GFPuL14eXi66V96xBWY73Y9PfR.jpg"
    },
    {
        "title": "Smile",
        "year": "2022",
        "rating": 7.2,
        "genres": ["Horror", "Mystery", "Thriller"],
        "horror_category": "jumpscare",  # Jump scare focused
        "intensity_level": 3,
        "overview": "After witnessing a bizarre, traumatic incident, Dr. Rose Cotter starts experiencing frightening occurrences.",
        "vote_average": 6.5,
        "poster_path": "/aPqcQwu4VGEewPhagWNncDbJ9Xp.jpg"
    },
    {
        "title": "Together",
        "year": "2021",
        "rating": None,  # Will be predicted
        "genres": ["Horror", "Drama"],
        "horror_category": "creepy",
        "intensity_level": 2,
        "overview": "A pandemic horror story.",
        "vote_average": 6.2,
        "poster_path": "/oeocQg0Bhmy0pqqRy50wEo0iwFB.jpg"
    },
    {
        "title": "The Platform 2", 
        "year": "2024",
        "rating": None,  # Will be predicted
        "genres": ["Horror", "Sci-Fi", "Thriller"],
        "horror_category": "gory",  # Violent dystopian horror
        "intensity_level": 4,
        "overview": "Sequel to the dystopian thriller.",
        "vote_average": 5.8,
        "poster_path": "/tvIpBg12IIA5Dr9Sjn38ygS1vQp.jpg"
    },
    {
        "title": "Cobweb",
        "year": "2023", 
        "rating": None,  # Will be predicted
        "genres": ["Horror", "Mystery"],
        "horror_category": "mysterious",
        "intensity_level": 3,
        "overview": "A young boy hears mysterious sounds from within the walls.",
        "vote_average": 6.1,
        "poster_path": "/cGXFosYUHYjjdKrOmA0bbjvzhKz.jpg"
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
        """Calculate user statistics including horror category preferences"""
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
            
            # Count horror categories
            horror_category_counts = {}
            horror_category_ratings = {}
            
            for movie in rated_movies:
                category = movie.get('horror_category', 'unknown')
                rating = movie['rating']
                
                horror_category_counts[category] = horror_category_counts.get(category, 0) + 1
                if category not in horror_category_ratings:
                    horror_category_ratings[category] = []
                horror_category_ratings[category].append(rating)
            
            # Calculate average rating per category
            category_preferences = {}
            for category, ratings in horror_category_ratings.items():
                avg_category_rating = sum(ratings) / len(ratings)
                category_preferences[category] = {
                    'count': horror_category_counts[category],
                    'avg_rating': round(avg_category_rating, 1)
                }
            
            # Sort by average rating
            top_horror_categories = sorted(
                category_preferences.items(), 
                key=lambda x: x[1]['avg_rating'], 
                reverse=True
            )[:4]
            
        else:
            avg_rating = 0
            top_genres = []
            top_horror_categories = []
        
        return {
            "total_movies": len(all_movies),
            "rated_movies": len(rated_movies),
            "unrated_movies": len(unrated_movies),
            "average_rating": round(avg_rating, 1),
            "top_genres": [{"genre": g[0], "count": g[1]} for g in top_genres],
            "horror_category_preferences": [
                {
                    "category": cat[0], 
                    "count": cat[1]['count'], 
                    "avg_rating": cat[1]['avg_rating']
                } 
                for cat in top_horror_categories
            ]
        }