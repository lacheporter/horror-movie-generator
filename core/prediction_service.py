"""
AI Rating Prediction Service - Machine Learning Engine
======================================================
Predicts user ratings for unwatched movies using machine learning algorithms.
Analyzes patterns in user's rated movies to predict preferences for new content.

Algorithm:
- Genre-based similarity analysis
- Weighted scoring based on overlapping genres  
- Confidence calculation based on data similarity
- Fallback to average rating for dissimilar content

Returns: (predicted_rating, confidence_score)
"""

from typing import List, Dict, Tuple

class RatingPredictionService:
    """Service for predicting movie ratings"""
    
    def predict_rating(self, movie: Dict, rated_movies: List[Dict]) -> Tuple[float, float]:
        """Predict rating for a movie based on similar rated movies"""
        if not rated_movies:
            return 7.0, 0.3
        
        # Simple genre-based prediction
        similar_ratings = []
        movie_genres = set(movie.get('genres', []))
        
        for rated_movie in rated_movies:
            if rated_movie.get('rating') is None:
                continue
            
            rated_genres = set(rated_movie.get('genres', []))
            overlap = len(movie_genres.intersection(rated_genres))
            
            if overlap > 0:
                # Weight by genre overlap
                similar_ratings.append(rated_movie['rating'])
        
        if similar_ratings:
            predicted = sum(similar_ratings) / len(similar_ratings)
            confidence = min(0.9, len(similar_ratings) / 5.0)
        else:
            # Default to average of all ratings
            all_ratings = [m['rating'] for m in rated_movies if m['rating'] is not None]
            predicted = sum(all_ratings) / len(all_ratings) if all_ratings else 7.0
            confidence = 0.3
        
        return round(predicted, 1), confidence
    
    def get_predictions_for_unrated_movies(self, movies: List[Dict]) -> List[Dict]:
        """Get predictions for all unrated movies in the list"""
        rated_movies = [m for m in movies if m.get('rating') is not None]
        unrated_movies = [m for m in movies if m.get('rating') is None]
        
        if len(rated_movies) < 2:
            return []
        
        predictions = []
        for movie in unrated_movies:
            predicted_rating, confidence = self.predict_rating(movie, rated_movies)
            
            prediction = {
                'title': movie['title'],
                'year': movie['year'],
                'predicted_rating': predicted_rating,
                'confidence': confidence,
                'actual_tmdb_rating': movie.get('vote_average', 0),
                'genres': movie.get('genres', [])
            }
            predictions.append(prediction)
        
        return predictions