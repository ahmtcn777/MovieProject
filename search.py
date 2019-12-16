import requests
from bs4 import BeautifulSoup
import os
from Movie import Movie
import json
imdbUrl = 'https://www.imdb.com/find?q='
movies = []


def searchKey(key, page=1):
    movies.clear()
    key = key.replace(" ", "%20")
    moviesSearchUrl = 'http://www.omdbapi.com/?apikey=b517ca2&s='+key
    movieSearchUrl = 'http://www.omdbapi.com/?apikey=b517ca2&i='
    r = requests.get(moviesSearchUrl,
                     params={"type": "movie",
                             "plot": "full",
                             "page": page})
    if("Error" not in str(r.content)):
        searchResult = json.loads(r.content)["Search"]
        for item in searchResult:
            mId = item["imdbID"]
            req = requests.get(movieSearchUrl+mId,
                               params={"type": "movie",
                                       "plot": "short",
                                       "r": "json"})
            responseJson = json.loads(req.content)
            imdbId = responseJson["imdbID"]
            imageUrl = responseJson["Poster"]
            movieName = responseJson["Title"]
            year = responseJson["Year"]
            ratings = responseJson["Ratings"]
            rate = ""
            genre = responseJson["Genre"]
            for item in ratings:
                if("Internet Movie Database" in item["Source"]):
                    rate = item["Value"]
            movie = Movie(imdbId,
                          imageUrl,
                          movieName,
                          year,
                          rate,
                          genre)
            movies.append(movie)
    return movies


if __name__ == "__main__":
    searchKey("batman begins", 1)
    for item in movies:
        print(item.name)
