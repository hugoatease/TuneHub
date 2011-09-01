import sys
from os import system

import datastruct

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