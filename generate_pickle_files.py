# generate_pickle_files.py

import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import ast

# Load datasets
movies = pd.read_csv("./Datasets/tmdb_5000_movies.csv")
credits = pd.read_csv("./Datasets/tmdb_5000_credits.csv")

# Merge and clean
movies = movies.merge(credits, on="title")
movies = movies[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]
movies.dropna(inplace=True)

# JSON string to list
def convert(obj):
    return [i["name"] for i in ast.literal_eval(obj)]

def convert3(obj):
    return [i["name"] for i in ast.literal_eval(obj)[:3]]

def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            return [i["name"]]
    return []

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert3)
movies["crew"] = movies["crew"].apply(fetch_director)
movies["overview"] = movies["overview"].apply(lambda x: x.split())

# Remove spaces
for feature in ["genres", "keywords", "cast", "crew"]:
    movies[feature] = movies[feature].apply(lambda x: [i.replace(" ", "") for i in x])

# Tags column
movies["tags"] = movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]
new_df = movies[["movie_id", "title", "tags"]]
new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x).lower())

# Stemming
ps = PorterStemmer()
def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])
new_df["tags"] = new_df["tags"].apply(stem)

# Vectorization and similarity
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df["tags"]).toarray()
similarity = cosine_similarity(vectors)

# Save .pkl files
pickle.dump(new_df, open("movie.pkl", "wb"))
pickle.dump(new_df.to_dict(), open("movie_dict.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("✅ movie.pkl, movie_dict.pkl, and similarity.pkl created successfully.")
