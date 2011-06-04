class Structure:
    
    def __init__(self):
        self.dic = {'Artist': None, 'Title': None, 'Provider': None, 'Lyric': None, 'Filename': None, 'Cached': None}
        
    def Artist(self, artist):
        self.dic['Artist'] = artist
        return self.dic
    
    def Title(self, title):
        self.dic['Title'] = title
        return self.dic
    
    def Provider(self, provider):
        self.dic['Provider'] = provider
        return self.dic
    
    def Lyric(self, lyric):
        self.dic['Lyric'] = lyric
        return self.dic
    
    def Filename(self, filename):
        self.dic['Filename'] = filename
        return self.dic
    
    def Cached(self, cached):
        self.dic['Cached'] = cached
        return self.dic
    
    def get(self):
        return self.dic
    
class Listing:
    
    def __init__(self, listing=None):
        if listing == None:
            self.listing = []
        else:
            self.listing = listing
        
    def add(self, data):
        self.listing.append(data)
        
    def remove(self, data):
        self.listing.remove(data)
        
    def get(self):
        return self.listing