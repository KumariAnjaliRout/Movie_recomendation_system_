# Movie_recomendation_system_
---
title: Movie Recommendation System
emoji: 🍿
colorFrom: yellow
colorTo: yellow
sdk: streamlit
sdk_version: 1.40.2
app_file: app.py
pinned: false
---

# Movie Recommender System  

## Project Overview  
This is a content-based movie recommender system built using Python, Pandas, and Streamlit. It uses vectorization techniques to recommend movies based on their features like genres, overview, and cast.  

## Features  
- Content-based filtering for personalized movie recommendations.  
- Interactive web interface built using Streamlit.  
- Fetches movie posters dynamically using the IMDb API.  
- Deployed on Hugging Face Spaces.  

## Dataset  
Dataset: [TMDB Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)  
Contains metadata for up to 5000 movies, including genres, overview, cast, and crew.  

## Technologies Used  
- **Python**: For data processing and building the recommendation logic.  
- **Pandas**: For dataset manipulation.  
- **Streamlit**: For creating the web app.  
- **Vectorization**: To compute movie similarities using techniques like TF-IDF.  
- **IMDb API**: To fetch movie posters dynamically, enriching the user experience.  

## Modules and Their Roles  

### **1. Data Loading and Preprocessing**  
- This module is responsible for loading the TMDB dataset and preparing it for use.  
- Tasks include handling missing values, cleaning data, and extracting relevant features like genres, overview, and cast.  

### **2. Vectorization Module**  
- Converts text-based features such as movie overviews into numerical vectors using techniques like TF-IDF (Term Frequency-Inverse Document Frequency).  
- This module computes similarity scores between movies, which are critical for generating recommendations.  

### **3. Recommendation Engine**  
- This core module applies content-based filtering logic.  
- It uses the similarity scores to identify and recommend movies that are most similar to a user's selected movie.  

### **4. Web Interface**  
- Built with Streamlit, this module provides an interactive and user-friendly interface.  
- Users can search for a movie, view its details, and get personalized recommendations instantly.  
- Fetches movie posters using the IMDb API, making recommendations visually engaging.

- ## Deployment  
The project is deployed on Hugging Face Spaces. You can explore it here:  


Like this Hugging Face space? Feel free to try it out and share your feedback!  

## Future Enhancements  
- Add collaborative filtering to incorporate user behavior into recommendations.  
- Use additional APIs like TMDB for real-time movie metadata updates.  
- Improve scalability to handle larger datasets.  

## API Reference  
This project integrates the **IMDb API** from RapidAPI to fetch movie posters dynamically. For more details on the API, check out the [IMDb API documentation](https://rapidapi.com/apidojo/api/imdb8/).  

## Acknowledgments  
- [TMDB Movie Metadata Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)  
- [IMDb API](https://rapidapi.com/apidojo/api/imdb8/)
