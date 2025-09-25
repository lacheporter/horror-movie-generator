#!/usr/bin/env python3
"""
Command Line Interface - Interactive Movie Recommendation Tool
==============================================================
Provides a simple terminal-based interface with 3 options:
1. Get movie recommendations based on your watch history
2. Get AI-powered rating predictions for unrated movies  
3. Exit the application

Usage: python cli/main.py
"""

import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.recommendation_service import MovieRecommendationService
from core.prediction_service import RatingPredictionService
from data.movie_data import get_default_watched_movies

def main():
    """Main CLI application"""
    print("🎬 Movie Recommendation System")
    print("=" * 50)
    
    # Get API key from environment
    api_key = os.getenv('TMDB_API_KEY', 'bfdf5ab47bb3b5e2b7beab4f21b4b97f')
    
    # Initialize services
    try:
        recommendation_service = MovieRecommendationService(api_key)
        prediction_service = RatingPredictionService()
        
        # Load default watched movies
        watched_movies_data = get_default_watched_movies()
        
        print(f"✅ Loaded {len(watched_movies_data)} movies")
        print()
        
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return

    while True:
        print("\nWhat would you like to do?")
        print("1. Get movie recommendations")
        print("2. Get rating predictions")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            get_recommendations(recommendation_service)
        elif choice == '2':
            get_predictions(prediction_service)
        elif choice == '3':
            print("👋 Thanks for using Movie Recommendation System!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

def get_recommendations(recommendation_service):
    """Get and display movie recommendations"""
    print("\n🎯 Getting your movie recommendations...")
    
    try:
        from data.movie_data import MovieDataService
        movies = MovieDataService.get_all_movies()
        
        recommendations = recommendation_service.get_recommendations_for_movies(movies, limit=10)
        
        if not recommendations:
            print("❌ No recommendations found. Try adding more movies to your watched list.")
            return
        
        print(f"\n🎬 Top {len(recommendations)} Movie Recommendations:")
        print("-" * 60)
        
        for i, movie in enumerate(recommendations, 1):
            title = movie.get('title', 'Unknown')
            year = movie.get('release_date', '')[:4] if movie.get('release_date') else 'Unknown'
            rating = movie.get('vote_average', 0)
            overview = movie.get('overview', 'No description available')
            
            print(f"{i:2d}. {title} ({year})")
            print(f"    ⭐ TMDB Rating: {rating}/10")
            print(f"    📝 {overview[:100]}...")
            print()
            
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")

def get_predictions(prediction_service):
    """Get and display rating predictions"""
    print("\n🔮 Predicting ratings for unrated movies...")
    
    try:
        from data.movie_data import MovieDataService
        movies = MovieDataService.get_all_movies()
        
        predictions = prediction_service.get_predictions_for_unrated_movies(movies)
        
        if not predictions:
            print("✅ All movies have ratings! No predictions needed.")
            return
        
        print(f"\n🔮 Rating Predictions:")
        print("-" * 60)
        
        # Sort predictions by predicted rating (highest first)
        predictions.sort(key=lambda x: x.get('predicted_rating', 0), reverse=True)
        
        for i, pred in enumerate(predictions, 1):
            title = pred.get('title', 'Unknown')
            year = pred.get('year', 'Unknown')
            predicted = pred.get('predicted_rating', 0)
            confidence = pred.get('confidence', 0) * 100  # Convert to percentage
            tmdb_rating = pred.get('actual_tmdb_rating', 0)
            
            print(f"{i:2d}. {title} ({year})")
            print(f"    🤖 Predicted Rating: {predicted:.1f}/10")
            print(f"    📊 Confidence: {confidence:.0f}%")
            print(f"    ⭐ TMDB Rating: {tmdb_rating:.1f}/10")
            print()
            
    except Exception as e:
        print(f"❌ Error making predictions: {e}")

if __name__ == "__main__":
    main()