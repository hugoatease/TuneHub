import datastruct
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