#!/usr/bin/env python3
"""
Project Structure Validation - System Integration Test
======================================================
Validates that the organized project structure works correctly.
Tests all imports, services, and core functionality to ensure
the refactoring didn't break anything.

Tests:
- Import validation for all modules
- Data service functionality  
- Prediction service accuracy
- Overall system integration

Usage: python test_structure.py
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported correctly"""
    print("🧪 Testing imports...")
    
    try:
        from data.movie_data import MovieDataService, get_default_watched_movies
        print("✅ data.movie_data - OK")
    except Exception as e:
        print(f"❌ data.movie_data - {e}")
        return False
    
    try:
        from core.tmdb_client import TMDBClient
        print("✅ core.tmdb_client - OK")
    except Exception as e:
        print(f"❌ core.tmdb_client - {e}")
        return False
    
    try:
        from core.recommendation_service import MovieRecommendationService
        print("✅ core.recommendation_service - OK")
    except Exception as e:
        print(f"❌ core.recommendation_service - {e}")
        return False
    
    try:
        from core.prediction_service import RatingPredictionService
        print("✅ core.prediction_service - OK")
    except Exception as e:
        print(f"❌ core.prediction_service - {e}")
        return False
    
    try:
        from api.models.movie_models import Movie, MovieRecommendation, RatingPrediction
        print("✅ api.models.movie_models - OK")
    except Exception as e:
        print(f"❌ api.models.movie_models - {e}")
        return False
    
    return True

def test_data_service():
    """Test the movie data service"""
    print("\n📊 Testing MovieDataService...")
    
    try:
        from data.movie_data import MovieDataService
        
        all_movies = MovieDataService.get_all_movies()
        rated_movies = MovieDataService.get_rated_movies()
        unrated_movies = MovieDataService.get_unrated_movies()
        stats = MovieDataService.get_user_stats()
        
        print(f"✅ Total movies: {len(all_movies)}")
        print(f"✅ Rated movies: {len(rated_movies)}")
        print(f"✅ Unrated movies: {len(unrated_movies)}")
        print(f"✅ User stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ MovieDataService test failed: {e}")
        return False

def test_prediction_service():
    """Test the prediction service"""
    print("\n🔮 Testing RatingPredictionService...")
    
    try:
        from core.prediction_service import RatingPredictionService
        from data.movie_data import MovieDataService
        
        service = RatingPredictionService()
        movies = MovieDataService.get_all_movies()
        
        predictions = service.get_predictions_for_unrated_movies(movies)
        print(f"✅ Generated {len(predictions)} predictions")
        
        if predictions:
            for pred in predictions[:2]:  # Show first 2 predictions
                print(f"   • {pred['title']} ({pred['year']}): {pred['predicted_rating']}/10")
        
        return True
        
    except Exception as e:
        print(f"❌ RatingPredictionService test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎬 Testing Movie Recommendation System - New Structure")
    print("=" * 60)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_data_service():
        success = False
    
    if not test_prediction_service():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! The new structure is working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    main()