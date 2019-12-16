import requests
from bs4 import BeautifulSoup
import os
from Movie import *
imdbUrl = 'https://www.imdb.com/chart/top/'
movies = []


def getTopList():
    r = requests.get(imdbUrl)
    source = BeautifulSoup(r.content, "html.parser")
    top250 = source.findAll("tbody", attrs={"class": "lister-list"})
    for tr in top250[0].findAll('tr'):
        td = tr.findAll('td')
        url = td[0].find('a').get('href')
        movieId = url.split("/")[2]
        img = td[0].find('a').find('img').get('src')
        if("_CR" in img):
            index = img.index("_CR")
            _img = img[:index-2] + "600"
            img = img[index:index+7] + '600,800_AL_.jpg'
            img = _img + img
        movieName = td[1].find('a').text
        year = td[1].find('span').text.replace('(', '').replace(')', '')
        score = td[2].find('strong').text
        movie = Movie(movieId, img, movieName, year, score, "")
        movies.append(movie)
    return movies


if __name__ == "__main__":
    getTopList()
