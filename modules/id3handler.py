import sys
sys.path.append('lib/')
sys.path.append('modules/')
import ID3v2
import ID3
from os import system
import datastruct

class ID3handler:
	
	def __init__(self, filename):
		self.filename = filename
		self.motorname = 'classic'
		
	def filter(self):
		ismp3 = '.mp3' in self.filename
		if ismp3 == False:
			self.motor = 'classic'
			return True
		else:
			return False
		
	def isMetagen(self):
		mutagenerror = False
		try:
			import mutagen
		except:
			mutagenerror = True
		
		if mutagenerror == False:
			self.motorname = 'mutagen'
			
	def initMotor(self):
		motorname = self.motorname
		
		if motorname == 'classic':
			motor = ClassicParsers(self.filename)
			self.motor = motor
		if motorname == 'mutagen':
			motor = Mutagen(self.filename)
			self.motor = motor
			
	def get(self):
		self.isMetagen()
		self.filter()
		self.initMotor()
		motor = self.motor
		dic = motor.get()
		return dic
				
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
		
	def get(self):
		structAPI = datastruct.Structure()
		self.getDataTuple()
		datatuple = self.mutagenData
		
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
			
			structAPI.Artist(artist)
			structAPI.Album(album)
			structAPI.Title(title)
			structAPI.Filename(self.filename)
			
			structure = structAPI.get()
			toreturn = structure
		else:
			toreturn = 0
		if (artist == None) or (title == None):
			toreturn = 0
		return toreturn
		
		
class ClassicParsers:

	def __init__(self, filename):
		self.filename = filename

	def getV2(self):
		mp3= self.filename
		try:
			id3 = ID3v2.ID3v2(filename=mp3)
		except :
			id3 = 0
		

		if id3 != 0:
			try:
				artistframe = id3.frames['TPE1']
				artistdata = artistframe.unpack()
				artist = artistdata['Text']

				titleframe = id3.frames['TIT2']
				titledata = titleframe.unpack()
				title = titledata['Text']
				
				try:
					albumframe = id3.frames['TALB']
					albumdata = albumframe.unpack()
					album = albumdata['Text']
				except:
					album = None

			except KeyError:
				artist = 0
			if artist == 0:
				return 0
			else:
				structAPI = datastruct.Structure()
				structAPI.Artist(artist)
				structAPI.Title(title)
				structAPI.Album(album)
				structAPI.Filename(self.filename)
				dic = structAPI.get()
				return dic

		else:
			return 0

	def getV1(self):
		structAPI = datastruct.Structure()
		mp3 = self.filename
		try:
			parser = ID3.ID3(mp3)
		except:
			parser = None
		if ( parser.has_key('ARTIST') and parser.has_key('TITLE') ) and parser != None:
			structAPI.Artist(parser['ARTIST'])
			structAPI.Title(parser['TITLE'])
			structAPI.Filename(self.filename)
			if parser.has_key('ALBUM'):
				structAPI.Album(parser['ALBUM'])
			dic = structAPI.get()
			return dic
		else:
			return 0

	def get(self):
		dic = self.getV1()
		if dic == 0:
			dic = self.getV2()
		return dic

	def writeLyrics(self,lyrics):
		command = self.id3v2bin + ' --USLT "' + lyrics + '" ' + self.filename
		system(command)