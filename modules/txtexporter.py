import datastruct
import os

class TxtExport:
    
    def __init__(self, songdata, destpath='export'):
        
        if os.path.isdir(destpath) == False:
            os.mkdir(destpath)
            
        self.structAPI = datastruct.Structure(songdata)
        self.destpath = destpath
        
    
    def escaping(self, filename):
        filename = filename.replace('/', '-')
	return filename
    
    
    def makeArtistDir(self):
        artist = self.structAPI.Artist()
        dirname = os.path.join(self.destpath, artist)
        if os.path.isdir(dirname) == False:
            os.mkdir(dirname)
        self.destpath = dirname
	
    def makeAlbumDir(self):
	album = self.structAPI.Album()
	if album != None:
	    self.destpath = os.path.join(self.destpath, album)
	    if os.path.isdir(self.destpath) == False:
		os.mkdir(self.destpath)
        
    def writeLyric(self):
        title = self.structAPI.Title()
        lyric = self.structAPI.Lyric()
	title = self.escaping(title)
        filename = os.path.join(self.destpath, title)
	filename = filename + '.txt'
	
	lyric = str(lyric)
	
	try:
	    f = open(filename, 'w')
            f.write(lyric)
            f.close()
	except:
	    pass
        
    def make(self):
        lyric = self.structAPI.Lyric()
        if lyric != None and lyric != 'Error':
            self.makeArtistDir()
	    self.makeAlbumDir()
            self.writeLyric()
