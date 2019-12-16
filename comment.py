import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import os

comments = []
RE_PATTERN = '[(]{1}[0-9]{4}[)]{1}'
driverPath = os.getcwd()+'\\phantomjs.exe'


def findMovie(movieName, year):
    comments.clear()
    r = requests.get('https://www.sinemalar.com/ara?q='+movieName +
                     '&type=movies')
    source = BeautifulSoup(r.content, 'html.parser')
    moviesDiv = source.findAll('div', attrs={'class': 'grid8'})
    for movie in moviesDiv:
        movieNameDiv = movie.findAll('div', attrs={'class': 'movie-name'})
        movieNameContent = movieNameDiv[0].find('a').text
        if(re.search(RE_PATTERN, movieNameContent) is not None):
            yearStart = re.search(RE_PATTERN, movieNameContent).start()
            yearEnd = re.search(RE_PATTERN, movieNameContent).end()
            movieYear = movieNameContent[yearStart:yearEnd]
            if(movieYear == '('+year+')'):
                return findComments(movieNameDiv[0].find('a').get('href'))
    return comments


def findComments(url):
    browser = webdriver.PhantomJS(executable_path=driverPath)
    browser.set_window_size(800, 600)
    browser.get(url)
    div = browser.find_element_by_css_selector('#comments')
    innerHTML = div.get_attribute('innerHTML')
    source = BeautifulSoup(innerHTML, 'html.parser')
    commentList = source.findAll('div', attrs={'class': 'content-list'})
    for comment in commentList:
        if(len(comment.findAll('a')) == 0):
            comments.append(comment.find('p').text.lstrip())
    browser.quit()
    return comments


def getMovieComments(movieId):
    comments.clear()
    movieId = movieId.replace('tt', '')
    r = requests.get('https://turkcealtyazi.org/mov/'+movieId+'/')
    source = BeautifulSoup(r.content, 'html.parser')
    commentDiv = source.findAll('div', attrs={'itemprop': 'review'})
    if(not len(commentDiv) > 0):
        return comments
    allCommentsLink = commentDiv[0].findAll('span',
                                            attrs={'class':
                                                   'nm-block-bottom'})[0]
    url = allCommentsLink.find('a').get('href')
    r = requests.get('https://turkcealtyazi.org'+url)
    source = BeautifulSoup(r.content, 'html.parser')
    commentDiv = source.findAll('div', attrs={'class': 'yorumlar2'})
    for comment in commentDiv:
        comments.append(comment.findAll('div', attrs={'class': 'ny8'})[0].text)
    return comments


if __name__ == "__main__":
    # url = findMovie('The Godfather', '1972')
    # if url is not None:
    # findComments(url)
    getMovieComments("tt0133093")
    print(len(comments))
