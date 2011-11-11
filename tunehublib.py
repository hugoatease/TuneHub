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

import pickle, os, sys, lyriclib, mutagen

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
    
class DirWalker(object):

    def walk(self,dir,meth):
    #walks a directory, and executes a callback on each file
                dir = os.path.abspath(dir)
                for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
                        nfile = os.path.join(dir,file)
                        meth(nfile)
                        if os.path.isdir(nfile):
                                try:
                                        self.walk(nfile,meth)
                                except OSError:
                                        pass

class Filer:
	def __init__(self, path):
		self.path = path
		
	def walkerCallback(self, filename):
		self.filelist.append(filename)
		
	def musiclist(self):
		from tunehubcore import dirwalker
		walker = dirwalker.DirWalker()
		self.filelist = []
		walker.walk(self.path, self.walkerCallback)
		return self.filelist
		
	def supportedList(self):
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

class LyricsFilter:
    
    def __init__(self, lyric):
        self.lyric = lyric
        self.result = False
        self.dontget = False
        
        if lyric == None:
            self.result = False
            self.dontget = True
        
    def instrumental(self):
        contain = False
        lines = self.lyric.count('\n')
        lyric = self.lyric.lower()
        
        if 'instrumental' in lyric:
            contain = True
            
        if contain == True and lines < 7:
            self.result = True
            
    def html(self):
        leftcount = self.lyric.count('<')
        rightcount = self.lyric.count('>')
        count = int( (leftcount + rightcount)/2 )
        
        if count > 4:
            self.result = True
            
    def get(self):
        if self.dontget == False:
            self.instrumental()
            self.html()
        return self.result
        
if __name__ == '__main__':
    lyric = raw_input('Lyric: ')
    motor = LyricsFilter(lyric)
    status = motor.get()
    print status
    
    if status == True:
        print 'These lyrics have triggered the instrumental or HTML filter'

class ID3handler:
	
	def __init__(self, filename):
		self.filename = filename
		
	def initMotor(self):
		motor = Mutagen(self.filename)
		self.motor = motor
			
	def get(self):
		self.initMotor()
		motor = self.motor
		dic = motor.get()
		return dic
	
	def writeLyrics(self, lyric):
		self.initMotor()
		motor = self.motor
		motor.writeLyrics(lyric)

class Mutagen:
	
	def getFormat(self):
		filename = self.filename
		if '.mp3' in filename:
			result = 'mp3'
		elif '.m4a' in filename:
			result = 'aac'
		elif '.ogg' in filename:
			result = 'vorbis'
		else:
			result = None
		
		return result
	
	def mutagenInit(self):
		format = self.format
		import mutagen
		self.mutagen = mutagen
		if format == 'mp3':
			import mutagen.mp3
			self.id3api = mutagen.mp3
		if format == 'aac':
			import mutagen.m4a
			self.id3api = mutagen.m4a
		if format == 'vorbis':
			import mutagen.oggvorbis
			self.id3api = mutagen.oggvorbis
	
	def __init__(self, filename):
		self.filename = filename
		self.id3api = None
		self.format = self.getFormat()
		self.mutagenInit()


	def getDataTuple(self):
		try:
			self.mutagenData = self.id3api.Open(self.filename)
		except:
			self.mutagenData = None
		
	def getMP3(self):
		structAPI = datastruct.Structure()
		datatuple = self.datatuple
		if self.mutagenData != None:
			
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
			toreturn = 0
		try:
			if (artist == None) or (title == None):
				toreturn = 0
		except UnboundLocalError:
			toreturn = 0
		return toreturn
	
	def getM4A(self):
		structAPI = datastruct.Structure()
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
			toreturn = 0
		if (artist == None) or (title == None):
			toreturn = 0
		return toreturn
		
	def get(self):
		toreturn = 0
		self.getDataTuple()
		self.datatuple = self.mutagenData
		if self.format == 'mp3':
			toreturn = self.getMP3()
		if self.format == 'aac':
			toreturn = self.getM4A()
		
		return toreturn
	
	def writeUSLT(self, lyrics):
		if self.format == 'mp3':
			mutagen = self.mutagen
			audio = mutagen.id3.ID3(self.filename)
			audio.add(mutagen.id3.USLT(encoding=3, lang=u'eng', text=lyrics))
			audio.save()
			
	def writeLyrics(self, lyrics):
		if self.format == 'mp3':
			self.writeUSLT(lyrics)

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

class TagExport:
    def __init__(self, item):
        structAPI = datastruct.Structure(item)
        self.filename = structAPI.Filename()
        self.lyric = structAPI.Lyric()
    
    def write(self):
        motor = id3handler.ID3handler(self.filename)
        try:
            motor.writeLyrics(self.lyric)
        except IOError:
            print '!!! Unable to write Lyrics for ' + self.filename

    def make(self):
        if self.lyric != None and len(self.filename)>1:
            status = self.filter()
            if status == False:
                self.write()
    
    def filter(self):
        api = LyricsFilter(self.lyric)
        status = api.get()
        return status

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

class Windows:
    
    def isWindows(self):
        if os.name == 'nt':
            return True
        else:
            return False
        
    def __init__(self, color='F0',title='LyricsFetcher'):
        iswin = self.isWindows()
        if iswin == True:
            self.windows = True
        else:
            self.windows = False
        
        self.colorname = color
        self.wintitle = title
            
    def color(self):
        if self.windows == True:
            cmd = 'color ' + self.colorname
            os.system(cmd)
            
    def title(self):
        if self.windows == True:
            cmd = 'title ' + self.wintitle
            os.system(cmd)
            
    def pause(self):
        if self.windows == True:
            os.system('pause')
            
    def begin(self):
        self.title()
        self.color()
        
    def end(self):
        self.pause()