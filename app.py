#!/usr/bin/env python3
"""
Movie Recommendation API - Main Application Entry Point
========================================================
This is the main FastAPI server that provides REST API endpoints for mobile app consumption.
Sets up CORS, includes movie routes, and provides health check endpoints.
Run this file to start the API server on http://localhost:8000

Usage: python app.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.movies import router as movies_router

# Initialize FastAPI app
app = FastAPI(
    title="Movie Recommendation API",
    description="API for movie recommendations and rating predictions",
    version="1.0.0"
)

# Enable CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes  
app.include_router(movies_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Movie Recommendation API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """API health status"""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)