import datastruct
import os

class TxtExport:
    
    def __init__(self, songdata, destpath='export'):
        
        if os.path.isdir(destpath) == False:
            os.mkdir(destpath)
            
        self.structAPI = datastruct.Structure(songdata)
        self.destpath = destpath
        
    
    def escaping(self, filename):
        pass
    
    
    def makeArtistDir(self):
        artist = self.structAPI.Artist()
        dirname = os.path.join(self.destpath, artist)
        if os.path.isdir(dirname) == False:
            os.mkdir(dirname)
        self.artistdir = dirname
        
    def writeLyric(self):
        title = self.structAPI.Title()
        lyric = self.structAPI.Lyric()
        filename = os.path.join(self.artistdir, title)
	filename = filename + '.txt'
        lyric = str(lyric)

        f = open(filename, 'w')
        f.write(lyric)
        f.close()
        
    def make(self):
        lyric = self.structAPI.Lyric()
        if lyric != None and lyric != 'Error':
            self.makeArtistDir()
            self.writeLyric()
