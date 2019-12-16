# Tutorial example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v57.0+

from cefpython3 import cefpython as cef
from top250 import getTopList
from search import searchKey
from Movie import Movie
from downloadMovie import downloadMovie, openExe
from subtitle import downloadSubtitle as download
from comment import findMovie, findComments, getMovieComments
import base64
import platform
import sys
import os
import threading
import codecs
import json
import asyncio
from setconfig import setConf

# HTML code. Browser will navigate to a Data uri created
# from this html code.
file = codecs.open("index.html", "r", encoding='utf8')
HTML_code = file.read()
page = 1
_searchKey = ""
movies = []
topCount = 0


def main():
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    # To change user agent use either "product_version"
    # or "user_agent" options. Explained in Tutorial in
    # "Change user agent string" section.
    settings = {
        # "product_version": "MyProduct/10.00",
        # "user_agent": "MyAgent/20.00 MyProduct/10.00",
    }
    cef.Initialize(settings=settings)
    set_global_handler()
    myBrowser = cef.CreateBrowserSync(url=html_to_data_uri(HTML_code),
                                      window_title="IMDB")
    global browser
    browser = myBrowser
    set_client_handlers(myBrowser)
    set_javascript_bindings(myBrowser)
    cef.MessageLoop()
    cef.Shutdown()


def html_to_data_uri(html, js_callback=None):
    # This function is called in two ways:
    # 1. From Python: in this case value is returned
    # 2. From Javascript: in this case value cannot be returned because
    #    inter-process messaging is asynchronous, so must return value
    #    by calling js_callback.
    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    return ret


def set_global_handler():
    # A global handler is a special handler for callbacks that
    # must be set before Browser is created using
    # SetGlobalClientCallback() method.
    global_handler = GlobalHandler()
    cef.SetGlobalClientCallback("OnAfterCreated",
                                global_handler.OnAfterCreated)


def set_client_handlers(browser):
    client_handlers = [LoadHandler(), DisplayHandler()]
    for handler in client_handlers:
        browser.SetClientHandler(handler)


def set_javascript_bindings(browser):
    external = External(browser)
    bindings = cef.JavascriptBindings(
        bindToFrames=False, bindToPopups=False)
    bindings.SetProperty("python_property", "This property was set in Python")
    bindings.SetProperty("cefpython_version", cef.GetVersion())
    bindings.SetFunction("html_to_data_uri", html_to_data_uri)
    bindings.SetFunction("searchMovie", searchMovie)
    bindings.SetFunction("searchMore", searchMore)
    bindings.SetFunction("searchResults", searchResults)
    bindings.SetFunction("topList", topList)
    bindings.SetFunction("topListResults", topListResults)
    bindings.SetFunction("deleteResults", deleteResults)
    bindings.SetFunction("downloadTorrent", downloadTorrent)
    bindings.SetFunction("downloadSubtitle", downloadSubtitle)
    bindings.SetFunction("getComments", getComments)
    bindings.SetFunction("printError", printError)
    bindings.SetObject("external", external)
    browser.SetJavascriptBindings(bindings)


def printError(content):
    browser.ExecuteFunction("printError", content)


def getComments(movieId):
    browser.ExecuteFunction("deleteComments")
    # index = movie.index(',')
    # movieName = movie[: index]
    # year = movie[index+1:]
    # print(movieName)
    # comments = findMovie(movieName, year)
    comments = getMovieComments(movieId)
    if(len(comments) > 0):
        for comment in comments:
            browser.ExecuteFunction("printComment", comment)
    else:
        printError("Yorum bulunamadı")


def downloadSubtitle(movie):
    index = movie.index(',')
    movieId = movie[: index]
    movieName = movie[index+1:].replace('%20', ' ')
    OK = download(movieId, movieName)
    if(not OK):
        printError("Altyazı bulunamadı")


def downloadTorrent(movieId):
    OK = downloadMovie(movieId)
    if(not OK):
        printError("Torrent bulunamadı")


def deleteResults():
    browser.ExecuteFunction("deleteResults")


def topList():
    global movies
    global topCount
    movies = getTopList()
    if(topCount == 0):
        while(topCount != 5):
            topListResults(movies[topCount])
            topCount += 1
    else:
        if(topCount <= len(movies)):
            if(topCount < len(movies)-5):
                _count = topCount
                while(topCount != _count+5):
                    topListResults(movies[topCount])
                    topCount += 1
            else:
                _count = len(movies)
                while(topCount != _count+1):
                    topListResults(movies[topCount])
                    topCount += 1


def topListResults(movie):
    browser.ExecuteFunction("topListResults", movie.movieId, movie.name,
                            movie.imageUrl, movie.year,
                            movie.score)


def searchMore():
    global page
    page += 1
    for movie in searchKey(_searchKey, page):
        searchResults(movie)


def searchMovie(key):
    global _searchKey
    _searchKey = key
    global page
    page = 1
    deleteResults()
    for movie in searchKey(key):
        searchResults(movie)


def searchResults(movie):
    browser.ExecuteFunction("searchResults", movie.movieId, movie.name,
                            movie.imageUrl, movie.year,
                            movie.score, movie.genre)


class GlobalHandler(object):
    def OnAfterCreated(self, browser, **_):
        """Called after a new browser is created."""
        # DOM is not yet loaded. Using js_print at this moment will
        # throw an error: "Uncaught ReferenceError: js_print is not defined".
        # We make this error on purpose. This error will be intercepted
        # in DisplayHandler.OnConsoleMessage.


class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""


class DisplayHandler(object):
    def OnConsoleMessage(self, browser, message, **_):
        """Called to display a console message."""
        # This will intercept js errors, see comments in OnAfterCreated


class External(object):
    def __init__(self, browser):
        self.browser = browser


if __name__ == '__main__':
    # asyncio.run(openExe())
    setConf()
    main()
