import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Download pickle files from Google Drive if not present
if not os.path.exists("movie_dict.pkl"):
    gdown.download("https://drive.google.com/uc?id=1Kw8CSC_ZmLGFQ-4f8ZgBvCs1mAFdG0ih", "movie_dict.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1qYThOUUMhkRtAWRyCFkO2EVCHEpYbFIz", "similarity.pkl", quiet=False)

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch poster
def fetch_poster(movie_name):
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q": movie_name}
    headers = {
        "x-rapidapi-key": "1fbfa1d6b2msh32cfe69cdbe3847p1a958ajsn576375deeb9c",
        "x-rapidapi-host": "imdb8.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            return results[0].get("image", {}).get("url", "https://via.placeholder.com/500x750?text=No+Poster")
    except:
        pass

    return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommendation logic
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = similarity[index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_posters = []

        for i in movie_list:
            title = movies.iloc[i[0]].title
            poster = fetch_poster(title)
            recommended_movies.append(title)
            recommended_posters.append(poster)

        return recommended_movies, recommended_posters
    except:
        return [], []

# Streamlit interface
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Select a movie you like:", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    if names:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
    else:
        st.warning("No recommendations found or movie not available.")
