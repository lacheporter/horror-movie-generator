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
        rated_movies = [m for m in movies if m.get('rating') is not None and m.get('rating') >= 7.0]
        if not rated_movies:
            # If no high-rated movies, use all rated movies
            rated_movies = [m for m in movies if m.get('rating') is not None]
            if not rated_movies:
                return []
        
        # Sort by rating and get recommendations for top movies
        top_movies = sorted(rated_movies, key=lambda x: x['rating'], reverse=True)[:3]
        
        for movie in top_movies:
            try:
                # Try multiple search variations for better matching
                movie_title = movie['title']
                search_variations = [
                    movie_title,
                    movie_title.replace('Seven', 'Se7en'),  # Handle Se7en vs Seven
                    movie_title.replace('IT', 'It'),        # Handle IT vs It
                ]
                
                movie_id = None
                for search_term in search_variations:
                    search_results = self.tmdb_client.search_movie(search_term)
                    if search_results:
                        # Try to find a match with the right year
                        movie_year = movie.get('year')
                        if movie_year:
                            for result in search_results:
                                result_year = result.get('release_date', '')[:4]
                                if result_year == str(movie_year):
                                    movie_id = result['id']
                                    break
                        
                        # If no year match, use the first result
                        if not movie_id:
                            movie_id = search_results[0]['id']
                        break
                
                if movie_id:
                    # Get recommendations and similar movies
                    recs = self.tmdb_client.get_movie_recommendations(movie_id, 8)
                    similar = self.tmdb_client.get_similar_movies(movie_id, 8)
                    
                    # Filter to horror/thriller movies
                    horror_genres = [27, 53, 9648]  # Horror, Thriller, Mystery
                    filtered_recs = []
                    
                    for rec in recs + similar:
                        genre_ids = rec.get('genre_ids', [])
                        if any(genre in horror_genres for genre in genre_ids):
                            filtered_recs.append(rec)
                    
                    all_recommendations.extend(filtered_recs)
                    
            except Exception as e:
                print(f"Error processing movie {movie['title']}: {e}")
                continue  # Skip movies that cause errors
        
        # Remove duplicates and return top results
        seen_titles = set()
        unique_recs = []
        for rec in all_recommendations:
            title = rec['title']
            if title not in seen_titles:
                seen_titles.add(title)
                unique_recs.append(rec)
                if len(unique_recs) >= limit:
                    break
        
        return unique_recs
    
    def get_random_horror_movies(self, watched_titles: set, limit: int = 10) -> List[Dict]:
        """Get random horror movies that the user hasn't watched"""
        import random
        
        all_random_movies = []
        horror_genre_id = 27  # Horror genre ID in TMDB
        
        # Get popular horror movies from multiple pages to increase randomness
        pages_to_fetch = min(5, max(2, limit // 10))  # Fetch 2-5 pages based on limit
        
        for page in range(1, pages_to_fetch + 1):
            try:
                # Discover horror movies with some variety
                horror_movies = self.tmdb_client.discover_movies(
                    with_genres=[horror_genre_id],
                    page=page,
                    sort_by='popularity.desc',
                    vote_average_gte=5.0,  # Only decent ratings
                    vote_count_gte=50      # Enough votes to be reliable
                )
                
                # Filter out movies the user has already watched
                unwatched_movies = []
                for movie in horror_movies:
                    movie_title = movie['title'].lower().strip()
                    if movie_title not in watched_titles:
                        # Add genre names for display
                        genre_names = self._get_genre_names_for_movie(movie)
                        movie['genre_names'] = genre_names
                        unwatched_movies.append(movie)
                
                all_random_movies.extend(unwatched_movies)
                
            except Exception as e:
                print(f"Error fetching horror movies from page {page}: {e}")
                continue
        
        # Randomly shuffle and return the requested number
        random.shuffle(all_random_movies)
        return all_random_movies[:limit]
    
    def spin_for_mood_movie(self, mood: str, watched_titles: set) -> Optional[Dict]:
        """Spin the roulette for a single movie based on emotional mood"""
        import random
        
        # Define mood-specific search parameters
        mood_config = {
            'gory': {
                'keywords': ['blood', 'gore', 'violent', 'brutal', 'slasher', 'torture'],
                'genres': [27, 53],  # Horror, Thriller
                'sort_preference': 'popularity.desc'
            },
            'creepy': {
                'keywords': ['psychological', 'disturbing', 'unsettling', 'paranormal', 'haunted'],
                'genres': [27, 9648, 53],  # Horror, Mystery, Thriller
                'sort_preference': 'vote_average.desc'
            },
            'mysterious': {
                'keywords': ['mystery', 'puzzle', 'investigation', 'detective', 'supernatural'],
                'genres': [9648, 27, 53],  # Mystery, Horror, Thriller
                'sort_preference': 'vote_average.desc'
            },
            'jumpscare': {
                'keywords': ['jump scare', 'sudden', 'startling', 'scary', 'frightening'],
                'genres': [27, 53],  # Horror, Thriller
                'sort_preference': 'popularity.desc'
            },
            'body-horror': {
                'keywords': ['body horror', 'transformation', 'mutation', 'grotesque', 'flesh', 'visceral', 'anatomical'],
                'genres': [27, 878, 53],  # Horror, Sci-Fi, Thriller
                'sort_preference': 'vote_average.desc'
            },
            'paranoid': {
                'keywords': ['paranoid', 'conspiracy', 'surveillance', 'persecution', 'madness', 'delusion', 'reality'],
                'genres': [27, 53, 9648],  # Horror, Thriller, Mystery
                'sort_preference': 'vote_average.desc'
            }
        }
        
        config = mood_config.get(mood, mood_config['gory'])
        all_mood_movies = []
        
        # Search across multiple pages for variety
        pages_to_search = 3
        
        for page in range(1, pages_to_search + 1):
            try:
                # Discover movies with mood-specific genres
                movies = self.tmdb_client.discover_movies(
                    with_genres=config['genres'],
                    page=page,
                    sort_by=config['sort_preference'],
                    vote_average_gte=5.5,  # Slightly higher threshold for single picks
                    vote_count_gte=100     # More votes for reliability
                )
                
                # Filter by keywords in overview and exclude watched movies
                mood_movies = []
                for movie in movies:
                    movie_title = movie['title'].lower().strip()
                    if movie_title not in watched_titles:
                        overview = movie.get('overview', '').lower()
                        
                        # Check if movie matches mood based on overview keywords
                        mood_score = 0
                        for keyword in config['keywords']:
                            if keyword in overview:
                                mood_score += 1
                        
                        # Include movies with keyword matches or high ratings for the mood
                        if mood_score > 0 or movie.get('vote_average', 0) >= 7.0:
                            # Add genre names for display
                            genre_names = self._get_genre_names_for_movie(movie)
                            movie['genre_names'] = genre_names
                            movie['mood_score'] = mood_score
                            mood_movies.append(movie)
                
                all_mood_movies.extend(mood_movies)
                
            except Exception as e:
                print(f"Error fetching {mood} movies from page {page}: {e}")
                continue
        
        if not all_mood_movies:
            return None
        
        # Sort by mood score and rating, then randomly pick from top candidates
        all_mood_movies.sort(key=lambda x: (x.get('mood_score', 0), x.get('vote_average', 0)), reverse=True)
        
        # Take top 20% or at least 5 movies for final random selection
        top_candidates = all_mood_movies[:max(5, len(all_mood_movies) // 5)]
        
        return random.choice(top_candidates)
    
    def _get_genre_names_for_movie(self, movie: Dict) -> List[str]:
        """Convert genre IDs to genre names"""
        genre_map = {
            27: 'Horror',
            53: 'Thriller',
            9648: 'Mystery',
            18: 'Drama',
            35: 'Comedy',
            28: 'Action',
            12: 'Adventure',
            16: 'Animation',
            80: 'Crime',
            99: 'Documentary',
            10751: 'Family',
            14: 'Fantasy',
            36: 'History',
            10402: 'Music',
            10749: 'Romance',
            878: 'Science Fiction',
            10770: 'TV Movie',
            10752: 'War',
            37: 'Western'
        }
        
        genre_ids = movie.get('genre_ids', [])
        return [genre_map.get(genre_id, 'Unknown') for genre_id in genre_ids if genre_id in genre_map]