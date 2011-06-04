from lyricsapi import Cache
from chartlyrics import *
from mldb import *
from sing365 import *
from sys import path
path.append('./sites/')
import datastruct

class Lyrics:
    
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.name = artist + ' - ' + title
        
        self.chartlyrics = ChartLyrics(artist, title)
        self.mldb = MLDB(artist, title)
        self.sing365 = Sing365(artist, title)
        self.cache = Cache()
        
    def getLyric(self):
        self.provider = 'Sing365'
        sing365 = self.sing365
        lyric = sing365.getLyric()
        self.cached = False
        if lyric == None:
            self.provider = 'MLDB'
            mldb = self.mldb
            lyric = mldb.getLyric()
            if lyric == None:
                self.provider = 'ChartLyrics'
                chartlyrics = self.chartlyrics
                lyric = chartlyrics.getLyric()
                if lyric == None:
                    self.provider = None
        
        self.lyric = lyric
        return lyric
    
    def get(self):
        self.getLyric()
        data = datastruct.Structure()
        data.Artist(self.artist)
        data.Title(self.title)
        data.Provider(self.provider)
        data.Lyric(self.lyric)
        data.Cached(self.cached)
        
        return data.get()