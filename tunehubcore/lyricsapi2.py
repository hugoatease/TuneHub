from tunehubcore import datastruct
from lyriclib import lyricsapi

class Lyrics:
    
    def __init__(self, cacheObject, artist, title, album=None, year=None):
        self.artist = artist
        self.title = title
        self.name = artist + ' - ' + title
        self.album = album
        self.year = year
        
        self.API = lyricsapi.API(artist, title)
        self.cache = cacheObject
        self.cache.setMeta(self.artist, self.title)
        
    def getLyric(self):
        Cache = self.cache
        Cache.openFile()
        cached_data = Cache.read()
        if cached_data == None:
            API=self.API
            lyric = API.get()
            try:
                self.provider = API.siteID
            except:
                self.provider = None
            self.cached = False
            if lyric == None:
                self.provider = None
                    
            self.lyric = lyric
            Cache.add(self.lyric, self.provider)
            return lyric
        else:
            self.cached = True
            self.provider = cached_data['Provider']
            self.lyric = cached_data['Lyric']
            
    
    def get(self):
        self.getLyric()
        data = datastruct.Structure()
        data.Artist(self.artist)
        data.Title(self.title)
        data.Album(self.album)
        data.Year(self.year)
        data.Provider(self.provider)
        data.Lyric(self.lyric)
        data.Cached(self.cached)
        
        return data.get()
