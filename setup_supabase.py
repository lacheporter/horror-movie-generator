#!/usr/bin/env python3
"""
Supabase Setup and Migration Script
===================================
Helps set up Supabase database and migrate existing data.
Run this after setting up your Supabase project.

Usage: python setup_supabase.py
"""

import os
import asyncio
from core.supabase_service import SupabaseService

async def main():
    print("🎬 NightReel - Supabase Setup")
    print("=" * 50)
    
    # Check environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase configuration!")
        print("\nPlease set the following environment variables in your .env file:")
        print("SUPABASE_URL=your_project_url")
        print("SUPABASE_ANON_KEY=your_anon_key")
        print("\nGet these from: https://app.supabase.com/project/YOUR_PROJECT/settings/api")
        return
    
    if 'your_supabase' in supabase_url.lower():
        print("❌ Please update your .env file with actual Supabase credentials!")
        return
    
    try:
        # Test connection
        print("🔌 Testing Supabase connection...")
        service = SupabaseService()
        
        # Try to get movies (this will test the connection)
        movies = await service.get_all_movies()
        print(f"✅ Connection successful! Found {len(movies)} movies in database.")
        
        # If no movies, offer to migrate sample data
        if not movies:
            print("\n📦 Database appears to be empty.")
            migrate = input("Would you like to migrate sample movie data? (y/n): ").lower().strip()
            
            if migrate == 'y':
                print("🔄 Migrating sample data...")
                await service.migrate_sample_data()
                
                # Verify migration
                movies = await service.get_all_movies()
                print(f"✅ Migration complete! Added {len(movies)} movies to database.")
            else:
                print("⏭️  Skipping migration. You can run this script again later.")
        else:
            print("✅ Database already contains movie data.")
        
        # Test basic operations
        print("\n🧪 Testing database operations...")
        
        # Test getting stats
        stats = await service.get_user_stats()
        print(f"📊 User stats: {stats['total_movies']} movies, avg rating: {stats['average_rating']}")
        
        # Test getting rated movies
        rated_movies = await service.get_rated_movies()
        print(f"⭐ Rated movies: {len(rated_movies)}")
        
        print("\n🎉 Supabase setup complete!")
        print("\nNext steps:")
        print("1. Update your API routes to use the database service")
        print("2. Test your application: python app.py")
        print("3. Test the frontend: python serve_frontend.py")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your Supabase URL and API key")
        print("2. Make sure you've run the SQL schema in your Supabase dashboard")
        print("3. Ensure your database has the 'user_movies' table")
        print("\nSQL schema file: schema.sql")

if __name__ == "__main__":
    asyncio.run(main())