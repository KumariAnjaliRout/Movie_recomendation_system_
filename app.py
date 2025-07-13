import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_name):
    """
    Fetch movie posters using the IMDb API via RapidAPI.
    Args:
        movie_name (str): The name of the movie for which to fetch the poster.
    Returns:
        str: The URL of the movie poster or a placeholder URL if not available.
    """
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q": movie_name}  # Search by movie name
    headers = {
        "x-rapidapi-key": "1fbfa1d6b2msh32cfe69cdbe3847p1a958ajsn576375deeb9c",  # Replace with your RapidAPI key
        "x-rapidapi-host": "imdb8.p.rapidapi.com"
    }

    try:
        
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()

       
        results = data.get("results", [])
        if results:
            poster_url = results[0].get("image", {}).get("url")  # Access the poster URL
            if poster_url:
                return poster_url
        st.warning("Poster not found for movie: {}".format(movie_name))
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"  # Placeholder image

    except requests.exceptions.Timeout:
        st.error("The request timed out while fetching poster for movie: {}".format(movie_name))
        return "https://via.placeholder.com/500x750?text=Timeout+Error"  # Timeout placeholder

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching poster for {movie_name}: {e}")
        return "https://via.placeholder.com/500x750?text=Connection+Error"  # Connection error placeholder


def recommend(movie):
    """
    Recommend movies based on similarity matrix and fetch posters using the IMDb API.
    Args:
        movie (str): The name of the movie for recommendations.
    Returns:
        list, list: Lists of recommended movie names and their poster URLs.
    """
    try:
        movies_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movies_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movie_list:
            recommended_movies.append(movies.iloc[i[0]].title)

            # Fetch poster and handle any connection or data issues
            poster = fetch_poster(movies.iloc[i[0]].title)
            recommended_movies_posters.append(poster)

        return recommended_movies, recommended_movies_posters

    except IndexError:
        st.error("The movie is not found in the dataset.")
        return [], []


# Load movie data and similarity matrix from pickled files
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

# Movie selection dropdown
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:", movies['title'].values
)

# Display recommendations upon button click
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    if names and posters and len(names) >= 5:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
    else:
        st.write("No recommendations found for the selected movie or unable to fetch posters.")
