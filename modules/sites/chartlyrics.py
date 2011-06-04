from urllib import quote
import urllib2
import xmltodict

class ChartLyrics:
	def __init__(self, artist, title):
		self.artist = artist
		self.title = title

	def search(self):
		url = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyric?artist=' + quote(self.artist) + '&song=' + quote(self.title)
		try:
			urlobj = urllib2.urlopen(url)
			xml = urlobj.read()
			urlobj.close()
		except urllib2.URLError:
			xml = 0
		if xml != 0:
			parsed = xmltodict.xmltodict(xml)
			try:
				parsed = parsed['SearchLyricResult'][0]
				lyricid = parsed['LyricId']
				lyricchecksum = parsed['LyricChecksum']
			except KeyError and TypeError:
				lyricid = 0
				parsed = 0
				lyricchecksum = 0

			if lyricid !=0:
				dic = {'ID': lyricid[0], 'Checksum': lyricchecksum[0]}
				self.lyricid = lyricid[0]
				self.lyricchecksum = lyricchecksum[0]
				return dic
			else:
				return None
		else:
			return None

	def getLyric(self):
		self.search()
		try:
			lyricid = self.lyricid
			checksum = self.lyricchecksum
		except AttributeError:
			lyricid = 0
			checksum = 0

		if lyricid != 0 and checksum != 0:
			url = 'http://api.chartlyrics.com/apiv1.asmx/GetLyric?lyricId=' + lyricid + '&lyricCheckSum=' + checksum
			try:
				urlobj = urllib2.urlopen(url)
				xml = urlobj.read()
				urlobj.close()
				parsed = xmltodict.xmltodict(xml)
				lyric = parsed['Lyric'][0]
				return lyric
				
			except urllib2.URLError:
				return None
		else:
			return None
