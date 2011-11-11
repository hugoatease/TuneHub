# -*- coding: utf-8 -*-
#    TuneHub Core Library.
#    Copyright (C) 2011  Hugo Caille
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

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
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Tunehub library is a Python module which includes most of the functions used to handle audio files, database management and lyrics fetching.

More information available on U{http://www.rockwire.tk}
'''

import pickle, os, sys, lyriclib

class Structure:
    '''Allows to handle dictionnaries of song metadata with functions.
    @cvar dic: Handled dictionnary of metadata.
    @type dic: dict'''
    dic = dict()
    
    def __init__(self, dic=None):
        '''@param dic: An existing metadata dictionnary.
        @type dic: dict'''
        if dic == None:
            self.dic = {'Artist': None, 'Album': None, 'Title': None, 'Year': None, 'Provider': None, 'Lyric': None, 'Filename': None, 'Cached': None}
        else:
            self.dic = dic
            
    def Artist(self, artist=None):
        '''@param artist: Artist's name to set.
        @type artist: str
        @return: Song's artist.
        @rtype: str'''
        if artist != None:
            self.dic['Artist'] = artist
            return self.dic
        else:
            return self.dic['Artist']
            
    def Album(self, album=None):
        '''@param album: Album's name to set.
        @type album: str
        @return: Song's album.
        @rtype: str'''
        if album != None:
            self.dic['Album'] = album
            return self.dic
        else:
            return self.dic['Album']
    
    def Title(self, title=None):
        '''@param title: Song's name to set.
        @type title: str
        @return: Song's title.
        @rtype: str'''
        if title != None:
            self.dic['Title'] = title
            return self.dic
        else:
            return self.dic['Title']
            
    def Year(self, year=None):
        '''@param year: Song's year to set.
        @type year: int
        @return: Song's year.
        @rtype: int'''
        if year != None:
            self.dic['Year'] = year
            return self.dic
        else:
            return self.dic['Year']
    
    def Provider(self, provider=None):
        '''@param provider: Provider's name to set.
        @type provider: str
        @return: Song's lyrics provider.
        @rtype: str'''
        if provider != None:
            self.dic['Provider'] = provider
            return self.dic
        else:
            return self.dic['Provider']
    
    def Lyric(self, lyric=None):
        '''@param lyric: Song's lyrics to set.
        @type lyric: str
        @return: Song's lyrics.
        @rtype: str'''
        if lyric != None:
            self.dic['Lyric'] = lyric
            return self.dic
        else:
            filterAPI = LyricsFilter( self.dic['Lyric'] )
            status = filterAPI.get()
            if status == False:
                return self.dic['Lyric']
            elif status == True:
                return None
    
    def Filename(self, filename=None):
        '''@param filename: Song's filename to set.
        @type filename: str
        @return: Song's filename.
        @rtype: str'''
        if filename != None:
            self.dic['Filename'] = filename
            return self.dic
        else:
            return self.dic['Filename']
    
    def Cached(self, cached=None):
        '''@param cached: Song's cached flag to set.
        @type cached: bool
        @return: Song's cached flag.
        @rtype: bool'''
        if cached != None:
            self.dic['Cached'] = cached
            return self.dic
        else:
            return self.dic['Cached']
    
    def get(self):
        '''@return: Metadata dictionnary
        @rtype: dict'''
        return self.dic
    
class Listing:
    '''Maintains a list of songs metadata.
    @cvar listing: Handled list of metadata dictionnaries
    @type listing: list'''
    listing = list()

    def __init__(self, listing=None):
        '''@param listing: An existing song list.
        @type listing: list'''
        if listing != None:
            self.listing = listing
        
    def add(self, metadata):
        '''Adds a metadata dictionnary to list
        @param metadata: Song's metadata to add.
        @type metadata: dict'''
        self.listing.append(metadata)
        
    def remove(self, metadata):
        '''Removes a metadata dictionnary to list
        @param metadata: Song's metadata to remove.
        @type metadata: dict'''
        self.listing.remove(metadata)
        
    def get(self):
        '''@return: Songs metadata's list.
        @rtype: list'''
        return self.listing

class Lyrics:
    '''Fetches lyrics with Lyriclib.
    @ivar api: Lyriclib API
    @type api: class
    @ivar cache: A L{Cache} object.
    @type cache: class
    @ivar inStruct: A L{Structure} containing metadata without lyrics.
    @type inStruct: class
    @cvar outStruct: A L{Structure} object containing inputed metadata and fetched ones.
    @type outStruct: class'''
    outStruct = Structure()
    
    def __init__(self, cacheObject, structure):
        '''Initializes L{inStruct}, L{Cache} and L{api}
        @param cacheObject: A L{Cache} object
        @type cacheObject: class
        @param structure: A L{Structure} containing metadata without lyrics.
        @type structure: class'''
        self.inStruct = Structure(structure)
        self.api = lyriclib.lyricsapi.API(self.inStruct.Artist(), self.inStruct.Title())
        self.cache = cacheObject
        self.cache.setMeta(self.inStruct.Artist(), self.inStruct.Title())
        
    def get(self):
        '''Fetches lyrics with Lyriclib, record them in L{Cache} and records results in L{outStruct}.
        @return: A L{Structure} object containing inputed metadata and fetched ones.
        @rtype: class'''
        self.outStruct.Artist(self.inStruct.Artist())
        self.outStruct.Title(self.inStruct.Title())
        self.outStruct.Album(self.inStruct.Album())
        self.outStruct.Year(self.inStruct.Year())
        cached_data = self.cache.read()
        if cached_data == None:
            lyric = self.api.get()
            try:
                self.outStruct.Provider(self.api.siteID)
            except:
                self.outStruct.Provider(None)
            self.outStruct.Cached(False)
            if lyric == None:
                self.outStruct.Provider(None)
            self.outStruct.Lyric(lyric)
            self.cache.add(self.outStruct.Lyric(), self.outStruct.Provider())
            return self.outStruct.get()
        else:
            self.outStruct.Cached(True)
            self.outStruct.Provider(cached_data['Provider'])
            self.outStruct.Lyric(cached_data['Lyric'])
        return self.outStruct.get()

class LyricsFilter:
    '''Determines if a string looks like lyrics.
    @ivar result: True if string seems to not being  lyrics and must be filtered, False if string seems to be lyrics.
    @type result: bool
    @cvar lyric: Lyrics string.
    @type lyric: str'''
    lyric = str()
    def __init__(self, lyric):
        '''Sets L{lyric}.
        @param lyric: The string to test
        @type lyric: str'''
        self.lyric = lyric
        self.result = False
        
        if lyric == None:
            self.result = False
        
    def instrumental(self):
        '''Determines if L{lyric} seems to be associated with an instrumental song, and updates L{result}.'''
        contain = False
        lines = self.lyric.count('\n')
        lyric = self.lyric.lower()
        
        if 'instrumental' in lyric:
            contain = True
            
        if contain == True and lines < 7:
            self.result = True
            
    def html(self):
        '''Determines if L{lyric} seems to be a html document, and updates L{result}.'''
        leftcount = self.lyric.count('<')
        rightcount = self.lyric.count('>')
        count = int( (leftcount + rightcount)/2 )
        
        if count > 4:
            self.result = True
            
    def get(self):
        '''Processes filtering operations and returns their results.
        @return: L{result} value.
        @rtype: bool'''
        if self.lyric != None:
            self.instrumental()
            self.html()
        return self.result

class Cache:
    '''Maintains a cache of already-fetched lyrics.
    @cvar filename: Cache database's filename.
    @ivar Artist: Artist matching lyrics to read or write into cache.
    @ivar Title: Title matching lyrics to read or write into cache.
    @ivar provider: Provider where lyrics were fetched.
    @ivar data: List of songs metadata dictionnaries, which can be parsed with L{Listing} and L{Structure}.
    @type Artist: str
    @type Title: str
    @type data: list
    @type provider: str'''
    filename = 'cache.db'

    def __init__(self, filename = 'cache.db'):
        '''@param filename: Cache database L{filename}.
        @type filename: str'''
        self.filename = filename
        self.openFile()
        
    def setMeta(self, artist, title):
        '''Set L{Artist} and L{Title} for next lyrics to add.
        @param artist: Song's artist name.
        @param title: Song's title.
        @type artist: str
        @type title: str'''
        self.Artist = artist
        self.Title = title
        
    def openFile(self):
        '''Parse the cache file with L{filename} as name and stores a song listing into L{data}''' 
        if os.path.isfile(self.filename) == False:
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
        '''Writes L{data} into file with L{filename} as filename.'''
        f = open(self.filename, 'w')
        pickle.dump(self.data, f)
        f.close()
        
    def add(self, lyrics, provider='Cache'):
        '''Adds lyrics corresponding to L{Artist} and L{Title} into cache.
        @param lyrics: Lyrics to add.
        @type lyrics: str
        @param provider: Provider's name.
        @type provider: str'''
        if lyrics != None:
            self.provider = provider
            structAPI = Structure()
            structAPI.Artist(self.Artist)
            structAPI.Title(self.Title)
            structAPI.Cached(True)
            structAPI.Provider(provider)
            structAPI.Lyric(lyrics)
            structure = structAPI.get()
            
            listAPI = Listing(self.data)
            listAPI.add(structure)
            self.data = listAPI.get()
            self.writeFile()
        
    def read(self):
        '''@return: Lyrics for L{Artist} and L{Title} which can be parsed by L{Structure}.'''
        structure = None
        for item in self.data:
            if item['Artist']==self.Artist and item['Title']==self.Title:
                lyric = item['Lyric']
                provider = item['Provider']
                structAPI = Structure()
                structAPI.Artist(self.Artist)
                structAPI.Title(self.Title)
                structAPI.Cached(True)
                structAPI.Provider(provider)
                structAPI.Lyric(lyric)
                structure = structAPI.get()
            
        return structure
    

class Filer:
    '''Provides a list of a path's supported audio files.
    @cvar path: Path to Walk for audio files.
    @type path: str
    @ivar filelist: List of all files in L{path}.
    @type filelist: list
    @ivar list: List of supported files in L{path}.
    @type list: list'''
    path = str()

    def __init__(self, path):
        '''@param path: Path to Walk for audio files.
        @type path: str'''
        self.path = path
	
    def walk(self,dir,meth):
        '''Walks a directory, and executes a callback on each file.
        @param dir: Directory to walk.
        @type dir: str
        @param meth: Callback to execute with file as argument.
        @type meth: function'''
        dir = os.path.abspath(dir)
        for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
                nfile = os.path.join(dir,file)
                meth(nfile)
                if os.path.isdir(nfile):
                        try:
                                self.walk(nfile,meth)
                        except OSError:
                                pass
            
    def walkerCallback(self, filename):
            '''Callback to execute with L{walk}.
            @param filename: File to append to L{filelist}.
            @type filename: str'''
            self.filelist.append(filename)
            
    def musiclist(self):
            '''Lists all files in L{path} and updates L{filelist}.
            @return: Lists of files in L{path}.
            @rtype: list'''
            walker = DirWalker()
            self.filelist = []
            self.walk(self.path, self.walkerCallback)
            return self.filelist
            
    def supportedList(self):
            '''Calls L{musiclist} and updates L{list}.
            @return: Supported files' filenames.
            @rtype: list'''
            self.musiclist()
            files = self.filelist
            list = []
            
            for file in files:
                    ismp3 = '.mp3' in file
                    ism4a = '.m4a' in file
                    isvorbis = '.ogg' in file
                    if ismp3 or ism4a or isvorbis:
                            list.append(file)
            self.list = list
            return list


class Mutagen:
    '''Retrieves metadata from an audio file with the Mutagen library
    @cvar filename: Supported audio file containing metadata
    @type filename: str
    @ivar mutagenData: Data retrieved from Mutagen
    @type mutagenData: dict
    @cvar mutagen: Mutagen module instance
    @ivar format: Audio File's format string returned by L{getFormat}
    @type format: str
    '''
    import mutagen
    mutagen = mutagen
    filename = str()

    def __init__(self, filename):
        '''@param filename: Supported audio file containing metadata.
        @type filename: str'''
        self.filename = filename
        self.format = self.getFormat(filename)

    def getFormat(self, filename):
        '''@param filename: Supported audio file containing metadata.
        @type filename: str
        @return: String representing an audio format name. Can be "mp3", "aac" or "vorbis"
        @rtype: str'''
        if '.mp3' in filename:
                return 'mp3'
        elif '.m4a' in filename:
                return 'aac'
        elif '.ogg' in filename:
                return 'vorbis'
        else:
                return None
    def getMeta(self):
        '''Gets a Metadata dictionnary with Mutagen from L{filename} and writes it in L{mutagenData}
        @return: Data retrieved from Mutagen.
        @rtype: dict'''
        try:
                self.mutagenData = self.mutagen.File(self.filename)
        except:
                self.mutagenData = None
        return self.mutagenData
            
    def getMP3(self):
        '''Parses information from L{mutagenData} for MP3 files.
        @return: L{Structure} with file's Metadata.
        @rtype: dict
        @require: L{mutagenData} must be a dict returned by L{getMeta}.'''
        structAPI = Structure()
        datatuple = self.mutagenData
        if datatuple!= None:
                
                try:
                        album = datatuple['TALB'][0]
                except:
                        album = None
                try:
                        title = datatuple['TIT2'][0]
                except:
                        title = None
                try:
                        artist = datatuple['TPE1'][0]
                except:
                        artist = None
                try:
                        year = int(unicode(datatuple['TDRC'][0]))
                        if year == 0:
                                year = None
                except:
                        year = None
                
                structAPI.Artist(artist)
                structAPI.Album(album)
                structAPI.Title(title)
                structAPI.Year(year)
                structAPI.Filename(self.filename)
                
                structure = structAPI.get()
                toreturn = structure
        else:
                toreturn = None
        try:
                if (artist == None) or (title == None):
                        toreturn = None
        except UnboundLocalError:
                toreturn = None
        return toreturn
    
    def getM4A(self):
        '''Parses information from L{mutagenData} for AAC files.
        @return: L{Structure} with file's Metadata.
        @rtype: dict
        @require: L{mutagenData} must be a dict returned by L{getMeta}.'''
        structAPI = Structure()
        datatuple = self.datatuple
        if self.mutagenData != None:
                
                try:
                        album = datatuple['\xa9alb']
                except:
                        album = None
                try:
                        title = datatuple['\xa9nam']
                except:
                        title = None
                try:
                        artist = datatuple['\xa9ART']
                except:
                        artist = None
                try:
                        year = int(unicode(datatuple['\xa9day']))
                        if year == 0:
                                year = None
                except:
                        year = None
                
                structAPI.Artist(artist)
                structAPI.Album(album)
                structAPI.Title(title)
                structAPI.Year(year)
                structAPI.Filename(self.filename)
                
                structure = structAPI.get()
                toreturn = structure
        else:
                toreturn = None
        if (artist == None) or (title == None):
                toreturn = None
        return toreturn
            
    def get(self):
        '''Generic method to make the Metadata fetching process.
        @return: L{Structure} with file's Metadata.
        @rtype: dict
        @require: L{mutagenData} must be a dict returned by L{getMeta}.'''
        toreturn = None
        self.getMeta()
        if self.format == 'mp3':
                toreturn = self.getMP3()
        if self.format == 'aac':
                toreturn = self.getM4A()
        
        return toreturn
    
    def writeUSLT(self, lyrics):
        '''Writes lyrics into a MP3 file
        @precondition: L{format} must be "mp3"'''
        if self.format == 'mp3':
                        audio = self.mutagen.id3.ID3(self.filename)
                        audio.add(self.mutagen.id3.USLT(encoding=3, lang=u'eng', text=lyrics))
                        audio.save()
    
    def writeLyrics(self, lyrics):
        '''Generic method to write lyrics into an audio file.
        @require: L{format} must be set with L{getFormat}.
        @param lyrics: Lyrics to write.
        @type lyrics: str'''
        self.getMeta()
        if self.format == 'mp3':
                self.writeUSLT(lyrics)

class TxtExport:
    '''Exports L{Structure} metadata into multiple text files
    @ivar structAPI: A L{Structure} object containing inputed song metadata.
    @type structAPI: class
    @ivar destpath: Export path, where Lyrics files will be stored.
    @type destpath: str
    @ivar mode: Export mode : "export" to write lyrics files inside directories with the Artist names and Album titles, "path" to write directly in a single path.
    @type mode: str
    @ivar lyric: Lyric to export.
    @type lyric: str'''
    def __init__(self, songdata, mode='export', destpath='export'):
        '''Sets L{structAPI}, L{destpath} and L{mode}.
        @param songdata: A L{Structure} object containing inputed song metadata.
        @type songdata: class
        @param mode: Export mode : "export" to write lyrics files inside directories with the Artist names and Album titles, "path" to write directly in a single path.
        @type mode: str
        @param destpath: Export path, where Lyrics files will be stored.
        @type destpath: str'''
        if os.path.isdir(destpath) == False:
            os.mkdir(destpath)
            
        self.structAPI = songdata
        self.destpath = destpath
        self.mode = mode
        
    
    def escaping(self, filename):
        '''Escapes filenames from ambigous characters
        @param filename: Original filename.
        @type filename: str
        @return: Escaped filename.
        @rtype: str'''
        filename = filename.replace('/', '-')
        return filename
    
    
    def makeArtistDir(self):
        '''Makes Artist directory inside L{destpath}, and CD the L{destpath}
        @return: Current destination path.
        @rtype: str'''
        artist = self.structAPI.Artist()
        artist = artist.encode('utf-8')
        dirname = os.path.join(self.destpath, artist)
        if os.path.isdir(dirname) == False:
            os.mkdir(dirname)
        self.destpath = dirname
        return self.destpath
        
    def makeAlbumDir(self):
        '''Makes Album directory inside L{destpath}, and CD the L{destpath}
        @return: Current destination path.
        @rtype: str'''
        album = self.structAPI.Album()
        if album != None:
            album = album.encode('utf-8')
            self.destpath = os.path.join(self.destpath, album)
            if os.path.isdir(self.destpath) == False:
                os.mkdir(self.destpath)
        return self.destpath
                
    def layout(self):
        '''Formats the L{lyric}.
        @return: Formatted lyric
        @rtype: str
        '''
        lyric = self.structAPI.Lyric()
        album = self.structAPI.Album()
        artist = self.structAPI.Artist()
        provider = self.structAPI.Provider()
        title = self.structAPI.Title()
        year = self.structAPI.Year()
        self.lyric = u'Artist: ' + unicode(artist) + u'\nTitle: ' + unicode(title) + u'\nAlbum: ' + unicode(album) + '\nYear: ' +unicode(year) + u'\nProvided by ' + unicode(provider) + u'\n\n' + unicode(lyric)
        return self.lyric
        
    def writeLyric(self):
        '''Layouts L{lyric} with L{layout} and writes it inside L{destpath}
        @return: Writed lyric filename.
        @rtype: str'''
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
        return filename
        
            
    def makeWindows(self):
        '''Runs the lyrics writing process on a Windows host.
        @attention: Must be run only if L{mode} is set on "export"
        @return: True if process succeed, False if it fails.
        @rtype bool'''
        lyric = self.structAPI.Lyric()
        if lyric != None and lyric != 'Error':
            try:
                self.makeArtistDir()
                self.makeAlbumDir()
                self.writeLyric()
                return True
            #except OSError:
                #pass
            except WindowsError:
                return False

    def makePOSIX(self):
        '''Runs the lyrics writing process on a POSIX host.
        @attention: Must be run only if L{mode} is set on "export".
        @return: True if process succeed, False if it fails.
        @rtype bool'''
        lyric = self.structAPI.Lyric()
        if lyric != None and lyric != 'Error':
            try:
                self.makeArtistDir()
                self.makeAlbumDir()
                self.writeLyric()
                return True
            except OSError:
                return False
            
    def makeByPath(self):
        '''Writes the lyrics without creating Artist/Album directories in L{destpath}.
        @attention: Must be run only if L{mode} is set on "path".
        @return: True if process succeed, False if it fails.
        @rtype bool'''
        lyric = self.structAPI.Lyric()
        filename = self.structAPI.Filename()
        self.destpath = os.path.dirname(filename)
        if lyric != None and lyric != 'Error':
            try:
                self.writeLyric()
                return True
            except OSError:
                return False
            
    def make(self):
        '''Generic method to make the lyric writing process. Calls L{makeByPath} if L{mode} is set to "path", or L{makePOSIX} or L{makeWindows} if L{mode} is set to "export", depending on the OS family.
        @return: True if process succeed, False if it fails.
        @rtype bool'''
        if self.mode == 'export':
            if os.name == 'nt':
                return self.makeWindows()
            else:
                return self.makePOSIX()
        if self.mode == 'path':
            return self.makeByPath()

class TagExport:
    '''Exports L{Structure} metadata into the corresponding file as a tag with Mutagen.
    @ivar filename: The file associated with the lyric.
    @type filename: str
    @ivar lyric: The lyric to export.
    @type lyric: str'''
    filename = str()
    
    def __init__(self, item):
        '''Sets L{filename} and L{lyric} with information contained in the inputed L{Structure}
        @param item: An L{Structure} object containing a lyric and filename'''
        structAPI = item
        self.filename = structAPI.Filename()
        self.lyric = structAPI.Lyric()
    
    def write(self):
        '''Writes lyrics into an audio file using Mutagen'''
        try:
            Mutagen(self.filename).writeLyrics(self.lyric)
        except IOError:
            print '!!! Unable to write Lyrics for ' + self.filename

    def make(self):
        '''Checks for lyrics validity with L{LyricsFilter}, then call L{write}'''
        if self.lyric != None and len(self.filename)>1:
            if LyricsFilter(self.lyric).get() == False:
                self.write()
