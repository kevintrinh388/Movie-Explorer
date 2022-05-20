"""
This python file contains functions involving the use of the wikipedia api
"""
import requests


def fetch_wiki(movie):
    """
    This function returns the link to a movie's wiki page
    """
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": movie,
        "format": "json",
        "formatversion": 2,
    }
    response = requests.get(base_url, params=params)
    response_json = response.json()
    query = response_json["query"]
    pages = query["pages"]
    first_page = pages[0]
    page_id = first_page["pageid"]
    link = f"https://en.wikipedia.org/?curid={page_id}"
    return link
