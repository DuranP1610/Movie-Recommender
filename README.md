A simple content-based movie recommender system built using Python.
It suggests similar movies based on the movie you select using TF-IDF vectorization and cosine similarity.

Features
Fetches movie data from TMDB API
Cleans and preprocesses movie dataset
Uses movie overviews to compute similarity
Recommends top similar movies based on input title
Simple Streamlit web interface

This project uses a content-based filtering approach:

Movie descriptions (overview) are converted into numerical vectors using TF-IDF
Similarity between movies is calculated using cosine similarity
When a user selects a movie, the system finds the most similar movies and recommends them

