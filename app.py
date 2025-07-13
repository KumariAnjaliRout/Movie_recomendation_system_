import gdown

# Download from Google Drive
movie_dict_url = "https://drive.google.com/file/d/1Kw8CSC_ZmLGFQ-4f8ZgBvCs1mAFdG0ih/view?usp=drive_link"
similarity_url = "https://drive.google.com/file/d/1qYThOUUMhkRtAWRyCFkO2EVCHEpYbFIz/view?usp=drive_link"

gdown.download(movie_dict_url, "movie_dict.pkl", quiet=False)
gdown.download(similarity_url, "similarity.pkl", quiet=False)

import streamlit as st
import pickle
import pandas as pd
import requests

#  Load saved movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

#  Function to fetch movie poster using IMDb API
def fetch_poster(movie_name):
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q": movie_name}
    headers = {
        "x-rapidapi-key": "1fbfa1d6b2msh32cfe69cdbe3847p1a958ajsn576375deeb9c",  # Replace with your own RapidAPI key
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

#  Movie Recommendation Function
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

#  Streamlit Web Interface
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
