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
import pickle
from os.path import isfile

class Cache:
    
    def __init__(self, filename = 'cache.db'):
        self.filename = filename
        self.openFile()
        
    def setMeta(self, artist, title):
        self.Artist = artist
        self.Title = title
        
    def openFile(self):
        if isfile(self.filename) == False:
            data = []
            f = open(self.filename, 'w')
            pickle.dump(data, f)
            f.close()
        else:
            f = open(self.filename, 'r')
            data = pickle.load(f)
            f.close()
            
        self.data = data
        
    def writeFile(self):
        f = open(self.filename, 'w')
        pickle.dump(self.data, f)
        f.close()
        
    def add(self, lyrics, provider='Cache'):
        if lyrics != 'Error':
            self.provider = provider
            structAPI = datastruct.Structure()
            structAPI.Artist(self.Artist)
            structAPI.Title(self.Title)
            structAPI.Cached(True)
            structAPI.Provider(provider)
            structAPI.Lyric(lyrics)
            structure = structAPI.get()
            
            listAPI = datastruct.Listing(self.data)
            listAPI.add(structure)
            self.data = listAPI.get()
            self.writeFile()
        
    def read(self):
        structure = None
        for item in self.data:
            if item['Artist']==self.Artist and item['Title']==self.Title:
                lyric = item['Lyric']
                provider = item['Provider']
                structAPI = datastruct.Structure()
                structAPI.Artist(self.Artist)
                structAPI.Title(self.Title)
                structAPI.Cached(True)
                structAPI.Provider(provider)
                structAPI.Lyric(lyric)
                structure = structAPI.get()
            
        return structure