import requests
from bs4 import BeautifulSoup
import os


def getMovieUrl(movieId):
    url = 'https://turkcealtyazi.org/mov/'+movieId[2:]+'/'
    r = requests.get(url)
    source = BeautifulSoup(r.content, 'html.parser')
    source = source.findAll("div", attrs={"class": "altsonsez2"})
    if(len(source) > 0):
        url = source[0].find('a').get('href')
        return url
    else:
        return None


def getSubtitle(url):
    r = requests.get('https://turkcealtyazi.org/'+url)
    source = BeautifulSoup(r.content, 'html.parser')
    source = source.find('div', attrs={'class': 'sub-container nleft'})
    source = source.find('form')
    source = source.findAll('input')
    idid = source[0].get('value')
    altid = source[1].get('value')
    sidid = source[2].get('value')
    data = {'idid': idid, 'altid': altid, 'sidid': sidid}
    response = requests.post('https://turkcealtyazi.org/ind', data)
    return response


def saveSubtitle(response, movieName):
    path = os.getcwd()+'\\subtitles\\'+movieName+'.zip'
    if(response.headers.get("Content-disposition")):
        open(path, 'wb').write(response.content)
        os.startfile(path)


def downloadSubtitle(movieId, movieName):
    url = getMovieUrl(movieId)
    if(url is not None):
        response = getSubtitle(url)
        saveSubtitle(response, movieName)
        return True
    else:
        return False


if __name__ == "__main__":
    downloadSubtitle('tt0068646', 'The Godfather')
