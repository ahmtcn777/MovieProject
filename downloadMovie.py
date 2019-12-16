from qbittorrent import Client
import os
import sys
import requests
from bs4 import BeautifulSoup
import asyncio
import subprocess as sp


def downloadMovie(movieId):
    r = requests.get('https://thepiratebay.org/search/' +
                     movieId+'/0/99/0')
    source = BeautifulSoup(r.content, "html.parser")
    td = source.findAll('td')
    if(len(td) > 0):
        magnet = td[1].findAll('a')[1].get('href')
        qb = Client('http://127.0.0.1:8080/')
        qb.download_from_link(magnet)
        return True
    else:
        return False


async def openExe():
    path = os.getcwd()+'\\qBittorrent\\qbittorrent.exe'
    sp.Popen(path, shell=True, stdin=None, stdout=None, stderr=None,
             close_fds=True)


if __name__ == "__main__":
    asyncio.run(downloadMovie('tt0111161'))
