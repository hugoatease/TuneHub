import datastruct
from pickle import load
from pickle import dump
from os.path import isfile

class Cache:
    
    def __init__(self, artist, title, filename = 'cache.db'):
        self.Artist = artist
        self.Title = title
        self.filename = filename
        
    def openFile(self):
        if isfile(self.filename) == False:
            data = []
            f = open(self.filename, 'w')
            dump(data, f)
            f.close()
        else:
            f = open(self.filename, 'r')
            raw = f.read()
            data = load(raw)
            f.close()
            
        self.data = data
        
    def writeFile(self):
        f = open(self.filename, 'w')
        dump(self.data, f)
        f.close()
        
    def add(self, lyrics, provider='Cache'):
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
        
    def read(self):
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