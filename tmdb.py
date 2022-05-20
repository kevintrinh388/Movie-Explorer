"""
This python file contains functions involving the use of the TMDB api
"""
import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
TMDB_KEY = os.getenv("TMDB_KEY")


def fetch_movie(movie):
    """
    This function returns the details of a movie
    """
    base_url = f"https://api.themoviedb.org/3/movie/{movie}"
    params = {"api_key": TMDB_KEY}
    response = requests.get(base_url, params=params)
    response_json = response.json()
    genre_list = response_json["genres"]
    genres = []
    for genre in genre_list:
        genres.append(genre["name"])
    image_link = "https://image.tmdb.org/t/p/w500/"
    details = {
        "title": response_json["title"],
        "tagline": response_json["tagline"],
        "genres": genres,
        "image": image_link + response_json["poster_path"],
    }
    return details
