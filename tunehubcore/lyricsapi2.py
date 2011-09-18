'''TuneHub Core Library.
    Copyright (C) 2011  Hugo Caille

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

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
