from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import db # Assuming db.py is in the same directory

app = FastAPI()

# Configure CORS to allow requests from your React frontend
# Adjust origins if your React app runs on a different port or domain
origins = [
    "http://localhost",
    "http://localhost:5173", # Default Vite development server port
    # Add any other origins where your frontend might be hosted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to EcoCycle ID API"}

@app.get("/waste_posts")
async def get_waste_posts_api():
    """
    Returns a list of all waste posts from the database.
    This endpoint currently does not support filtering.
    """
    posts = db.get_waste_posts()
    # Remove binary image data to prevent JSON serialization errors
    for post in posts:
        if 'image_blob' in post:
            del post['image_blob']
    return posts

@app.get("/waste_posts/filtered")
async def get_filtered_waste_posts_api(filters: str = None):
    """
    Returns a list of waste posts from the database, optionally filtered by suitability tags.
    Filters should be a comma-separated string (e.g., "Maggot BSF,Ayam/Unggas").
    """
    filter_list = []
    if filters:
        filter_list = [f.strip() for f in filters.split(',')]
    
    posts = db.get_waste_posts(filters=filter_list)
    # Remove binary image data to prevent JSON serialization errors
    for post in posts:
        if 'image_blob' in post:
            del post['image_blob']
    return posts

# You would run this API using a command like:
# uvicorn api:app --reload --port 8000
