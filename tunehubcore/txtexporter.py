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
import os

class TxtExport:
    
    def __init__(self, songdata, mode='export', destpath='export'):
        
        if os.path.isdir(destpath) == False:
            os.mkdir(destpath)
            
        self.structAPI = datastruct.Structure(songdata)
        self.destpath = destpath
        self.mode = mode
        
    
    def escaping(self, filename):
        filename = filename.replace('/', '-')
        return filename
    
    
    def makeArtistDir(self):
        artist = self.structAPI.Artist()
        artist = artist.encode('utf-8')
        dirname = os.path.join(self.destpath, artist)
        if os.path.isdir(dirname) == False:
            os.mkdir(dirname)
        self.destpath = dirname
        
    def makeAlbumDir(self):
        album = self.structAPI.Album()
        if album != None:
            album = album.encode('utf-8')
            self.destpath = os.path.join(self.destpath, album)
            if os.path.isdir(self.destpath) == False:
                os.mkdir(self.destpath)
                
    def layout(self):
        lyric = self.structAPI.Lyric()
        album = self.structAPI.Album()
        artist = self.structAPI.Artist()
        provider = self.structAPI.Provider()
        title = self.structAPI.Title()
        year = self.structAPI.Year()
        self.lyric = u'Artist: ' + unicode(artist) + u'\nTitle: ' + unicode(title) + u'\nAlbum: ' + unicode(album) + '\nYear: ' +unicode(year) + u'\nProvided by ' + unicode(provider) + u'\n\n' + unicode(lyric)
        
    def writeLyric(self):
        self.layout()
        title = self.structAPI.Title()
        lyric = self.lyric
        title = self.escaping(title)
        title = title.encode('utf-8')
        filename = os.path.join(self.destpath, title)
        filename = filename + '.txt'
        
        
        lyric = lyric.encode('utf-8')
        
        try:
            f = open(filename, 'w')
            f.write(lyric)
            f.close()
        except:
            print '!!! Unable to write Lyrics for ' + filename
        
            
    def makeWindows(self):
        lyric = self.structAPI.Lyric()
        if lyric != None and lyric != 'Error':
            try:
                self.makeArtistDir()
                self.makeAlbumDir()
                self.writeLyric()
            #except OSError:
                #pass
            except WindowsError:
                pass

    def makePOSIX(self):
        lyric = self.structAPI.Lyric()
        if lyric != None and lyric != 'Error':
            try:
                self.makeArtistDir()
                self.makeAlbumDir()
                self.writeLyric()
            except OSError:
                pass
            
    def makeByPath(self):
        lyric = self.structAPI.Lyric()
        filename = self.structAPI.Filename()
        self.destpath = os.path.dirname(filename)
        if lyric != None and lyric != 'Error':
            try:
                self.writeLyric()
            except OSError:
                pass
            
    def make(self):
        if self.mode == 'export':
            if os.name == 'nt':
                self.makeWindows()
            else:
                self.makePOSIX()
        if self.mode == 'path':
            self.makeByPath()