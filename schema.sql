-- Supabase Database Schema for Horror Movie Generator
-- Run these SQL commands in your Supabase SQL editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create user_movies table
CREATE TABLE user_movies (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL DEFAULT 'default',
    title VARCHAR(500) NOT NULL,
    year VARCHAR(4),
    rating DECIMAL(3,1) CHECK (rating >= 1 AND rating <= 10),
    genres JSONB DEFAULT '[]',
    horror_category VARCHAR(50),
    intensity_level INTEGER CHECK (intensity_level >= 1 AND intensity_level <= 5),
    overview TEXT,
    vote_average DECIMAL(3,1) DEFAULT 0,
    poster_path VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Ensure unique movie per user
    UNIQUE(user_id, title)
);

-- Create indexes for better performance
CREATE INDEX idx_user_movies_user_id ON user_movies(user_id);
CREATE INDEX idx_user_movies_rating ON user_movies(rating) WHERE rating IS NOT NULL;
CREATE INDEX idx_user_movies_category ON user_movies(horror_category);
CREATE INDEX idx_user_movies_title ON user_movies(title);

-- Enable Row Level Security (RLS)
ALTER TABLE user_movies ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS (users can only access their own movies)
CREATE POLICY "Users can view own movies" ON user_movies
    FOR SELECT USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'default');

CREATE POLICY "Users can insert own movies" ON user_movies
    FOR INSERT WITH CHECK (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'default');

CREATE POLICY "Users can update own movies" ON user_movies
    FOR UPDATE USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'default');

CREATE POLICY "Users can delete own movies" ON user_movies
    FOR DELETE USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub' OR user_id = 'default');

-- Create a function to automatically update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to auto-update updated_at
CREATE TRIGGER update_user_movies_updated_at 
    BEFORE UPDATE ON user_movies 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Optional: Create a view for easier movie statistics
CREATE VIEW user_movie_stats AS
SELECT 
    user_id,
    COUNT(*) as total_movies,
    COUNT(rating) as rated_movies,
    COUNT(*) - COUNT(rating) as unrated_movies,
    ROUND(AVG(rating), 1) as average_rating,
    MAX(updated_at) as last_activity
FROM user_movies 
GROUP BY user_id;

-- Insert sample data (optional - you can do this via the migration function instead)
/*
INSERT INTO user_movies (user_id, title, year, rating, genres, horror_category, intensity_level, overview, vote_average, poster_path) VALUES
('default', 'Copycat', '1995', 8.0, '["Horror", "Thriller", "Crime"]', 'creepy', 3, 'A psychological thriller about a serial killer copycat.', 6.6, '/oMgwJb016znNZcpDR20eXxZoW8A.jpg'),
('default', 'Seven', '1995', 9.0, '["Horror", "Thriller", "Crime"]', 'mysterious', 4, 'Two detectives hunt a serial killer who uses the seven deadly sins.', 8.6, '/f7CPfYN2bxr43Cr4fCYWjUKoVEs.jpg'),
('default', 'The Wailing', '2016', 9.0, '["Horror", "Mystery", "Thriller"]', 'mysterious', 4, 'A mysterious illness spreads in a remote Korean village.', 7.5, '/aXlL7yYwpXInhltamtzKQFBG08G.jpg');
*/