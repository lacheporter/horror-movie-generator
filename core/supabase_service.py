"""
Supabase Database Service - PostgreSQL Integration
=================================================
Handles all database operations using Supabase (PostgreSQL) backend.
Replaces the static data in movie_data.py with persistent storage.

Features:
- User movie ratings and watch history
- Movie metadata storage
- User statistics and preferences
- Real-time updates support
"""

import os
from typing import List, Dict, Optional
from supabase import create_client, Client
from datetime import datetime

class SupabaseService:
    """Service for Supabase database operations"""
    
    def __init__(self):
        # Get Supabase credentials from environment variables
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    # Movies table operations
    async def get_all_movies(self, user_id: str = "default") -> List[Dict]:
        """Get all movies for a user"""
        try:
            response = self.supabase.table('user_movies').select('*').eq('user_id', user_id).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching movies: {e}")
            return []
    
    async def get_movie_by_title(self, title: str, user_id: str = "default") -> Optional[Dict]:
        """Get a specific movie by title"""
        try:
            response = self.supabase.table('user_movies').select('*').eq('user_id', user_id).eq('title', title).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching movie {title}: {e}")
            return None
    
    async def add_or_update_movie(self, movie_data: Dict, user_id: str = "default") -> bool:
        """Add a new movie or update existing one"""
        try:
            movie_data['user_id'] = user_id
            movie_data['updated_at'] = datetime.now().isoformat()
            
            # Check if movie exists
            existing = await self.get_movie_by_title(movie_data['title'], user_id)
            
            if existing:
                # Update existing movie
                response = self.supabase.table('user_movies').update(movie_data).eq('id', existing['id']).execute()
            else:
                # Insert new movie
                movie_data['created_at'] = datetime.now().isoformat()
                response = self.supabase.table('user_movies').insert(movie_data).execute()
            
            return len(response.data) > 0
        except Exception as e:
            print(f"Error adding/updating movie: {e}")
            return False
    
    async def rate_movie(self, title: str, rating: float, user_id: str = "default") -> bool:
        """Rate a movie"""
        try:
            movie = await self.get_movie_by_title(title, user_id)
            if movie:
                response = self.supabase.table('user_movies').update({
                    'rating': rating,
                    'updated_at': datetime.now().isoformat()
                }).eq('id', movie['id']).execute()
                return len(response.data) > 0
            return False
        except Exception as e:
            print(f"Error rating movie {title}: {e}")
            return False
    
    async def remove_rating(self, title: str, user_id: str = "default") -> bool:
        """Remove rating from a movie"""
        try:
            movie = await self.get_movie_by_title(title, user_id)
            if movie:
                response = self.supabase.table('user_movies').update({
                    'rating': None,
                    'updated_at': datetime.now().isoformat()
                }).eq('id', movie['id']).execute()
                return len(response.data) > 0
            return False
        except Exception as e:
            print(f"Error removing rating from {title}: {e}")
            return False
    
    async def get_rated_movies(self, user_id: str = "default") -> List[Dict]:
        """Get only rated movies"""
        try:
            response = self.supabase.table('user_movies').select('*').eq('user_id', user_id).not_.is_('rating', None).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching rated movies: {e}")
            return []
    
    async def get_unrated_movies(self, user_id: str = "default") -> List[Dict]:
        """Get only unrated movies"""
        try:
            response = self.supabase.table('user_movies').select('*').eq('user_id', user_id).is_('rating', None).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching unrated movies: {e}")
            return []
    
    async def get_movies_by_category(self, category: str, user_id: str = "default") -> List[Dict]:
        """Get movies by horror category"""
        try:
            response = self.supabase.table('user_movies').select('*').eq('user_id', user_id).eq('horror_category', category).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching movies by category {category}: {e}")
            return []
    
    async def get_user_stats(self, user_id: str = "default") -> Dict:
        """Calculate user statistics"""
        try:
            all_movies = await self.get_all_movies(user_id)
            rated_movies = await self.get_rated_movies(user_id)
            unrated_movies = await self.get_unrated_movies(user_id)
            
            if rated_movies:
                avg_rating = sum(m['rating'] for m in rated_movies) / len(rated_movies)
                
                # Count genres
                genre_counts = {}
                for movie in rated_movies:
                    genres = movie.get('genres', [])
                    if isinstance(genres, list):
                        for genre in genres:
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
        except Exception as e:
            print(f"Error calculating user stats: {e}")
            return {
                "total_movies": 0,
                "rated_movies": 0,
                "unrated_movies": 0,
                "average_rating": 0,
                "top_genres": [],
                "horror_category_preferences": []
            }
    
    # Migration helper - populate database with existing sample data
    async def migrate_sample_data(self, user_id: str = "default"):
        """Migrate the existing sample data to Supabase"""
        from data.movie_data import WATCHED_MOVIES_DATA
        
        for movie in WATCHED_MOVIES_DATA:
            movie_data = {
                'title': movie['title'],
                'year': movie['year'],
                'rating': movie.get('rating'),
                'genres': movie['genres'],
                'horror_category': movie.get('horror_category'),
                'intensity_level': movie.get('intensity_level'),
                'overview': movie.get('overview', ''),
                'vote_average': movie.get('vote_average', 0),
                'poster_path': movie.get('poster_path')
            }
            await self.add_or_update_movie(movie_data, user_id)
        
        print(f"✅ Migrated {len(WATCHED_MOVIES_DATA)} movies to Supabase for user {user_id}")