import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

Base_url = "https://api.themoviedb.org/3"
movies = []


def get_genres():
    """Fetch genre mapping (id → name)"""
    url = f"{Base_url}/genre/movie/list"
    params = {"api_key": API_KEY}

    response = requests.get(url, params=params)
    data = response.json()

    return {g["id"]: g["name"] for g in data["genres"]}

genre_map = get_genres()
NUM_PAGES = 50
def fetch_movies():
    for page in range(1, NUM_PAGES + 1):
        

        url = f"{Base_url}/movie/popular"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "page": page
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("Error:", response.text)
            break

        data = response.json()

        for movie in data["results"]:
            movies.append({
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie["overview"],
                "rating": movie["vote_average"],
                "release_date": movie["release_date"],
                "genres": movie["genre_ids"],
                "poster_path": movie["poster_path"]
            })

        time.sleep(0.2)  # avoids rate limits

def clean_data():
    df = pd.DataFrame(movies)

    # Convert genre IDs → names
    def convert_genres(genre_ids):
        return [genre_map.get(i, "") for i in genre_ids]

    df["genres"] = df["genres"].apply(convert_genres)

    # Drop empty overviews (important for recommender)
    df = df[df["overview"].str.len() > 0]

    return df

if __name__ == "__main__":
    fetch_movies()
    df = clean_data()

    df.to_csv("movies.csv", index=False)

    print("\nSaved dataset!")
    #print(df.head())

