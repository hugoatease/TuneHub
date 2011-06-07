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

	def basicInfov2(self):
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

	def basicInfov1(self):
		structAPI = datastruct.Structure()
		mp3 = self.filename
		parser = ID3.ID3(mp3)
		if parser.has_key('ARTIST') and parser.has_key('TITLE'):
			structAPI.Artist(parser['ARTIST'])
			structAPI.Title(parser['TITLE'])
			structAPI.Filename(self.filename)
			if parser.has_key('ALBUM'):
				structAPI.Album(parser['ALBUM'])
			dic = structAPI.get()
			return dic
		else:
			return 0

	def basicInfo(self):
		dic = self.basicInfov1()
		if dic == 0:
			dic = self.basicInfov2()
		return dic

	def writeLyrics(self,lyrics):
		command = self.id3v2bin + ' --USLT "' + lyrics + '" ' + self.filename
		system(command)
