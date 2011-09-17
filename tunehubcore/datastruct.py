from tunehubcore import filter

class Structure:
    
    def __init__(self, dic=None):
        if dic == None:
            self.dic = {'Artist': None, 'Album': None, 'Title': None, 'Year': None, 'Provider': None, 'Lyric': None, 'Filename': None, 'Cached': None}
        else:
            self.dic = dic
            
    def Artist(self, artist=None):
        if artist != None:
            self.dic['Artist'] = artist
            return self.dic
        else:
            return self.dic['Artist']
            
    def Album(self, album=None):
        if album != None:
            self.dic['Album'] = album
            return self.dic
        else:
            return self.dic['Album']
    
    def Title(self, title=None):
        if title != None:
            self.dic['Title'] = title
            return self.dic
        else:
            return self.dic['Title']
            
    def Year(self, year=None):
        if year != None:
            self.dic['Year'] = year
            return self.dic
        else:
            return self.dic['Year']
    
    def Provider(self, provider=None):
        if provider != None:
            self.dic['Provider'] = provider
            return self.dic
        else:
            return self.dic['Provider']
    
    def Lyric(self, lyric=None):
        if lyric != None:
            self.dic['Lyric'] = lyric
            return self.dic
        else:
            filterAPI = filter.LyricsFilter( self.dic['Lyric'] )
            status = filterAPI.get()
            if status == False:
                return self.dic['Lyric']
            elif status == True:
                return None
    
    def Filename(self, filename=None):
        if filename != None:
            self.dic['Filename'] = filename
            return self.dic
        else:
            return self.dic['Filename']
    
    def Cached(self, cached=None):
        if cached != None:
            self.dic['Cached'] = cached
            return self.dic
        else:
            return self.dic['Cached']
    
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