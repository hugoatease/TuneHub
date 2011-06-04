# lyricsapi.py version 1
# This API is a part of the Lyrics Fetcher Suite

# Module for retrieving song lyrics from popular lyrics websites

# Copyright 2011 Hugo Caille <hugo@gkz.fr.nf>
# This work is released under the GNU GPL version 3.

__author__="Hugo Caille"
__version__="1.0"

import urllib2
import xmltodict
from urllib import quote
import pickle
from os.path import isfile
import sys

sys.path.append('./modules/sites')
from chartlyrics import *
from mldb import *
from sing365 import *

class Lyrics:

	def getLyric(self):
		artist = self.artist
		title = self.title
		artist2 = artist.lower()
		title2 = title.lower()
		cache = Cache()
		cached = cache.read(artist, title)
		if cached != 0:
			return cached
		else:

			chart = ChartLyrics(artist2, title2)
			lyric = chart.getLyric()
			provider = 'chartlyrics.com'
			if lyric == 0:
				mldb = MLDB(artist2,title2)
				lyric = mldb.getLyric()
				provider = 'mldb.org'

			if lyric != 0:
				dic = {'Artist': artist, 'Title': title, 'Provider': provider, 'Lyrics': lyric}
				cache.add(dic)
				return dic

			else:
				dic = {'Artist': artist, 'Title': title, 'Provider': None, 'Lyrics': None}
				cache.add(dic)
				return 0

class Cache:
	def __init__(self):
		if isfile('cache.db') == False:
			struct = []
			f = open('cache.db','w')
			pickle.dump(struct,f)
			f.close()

	def add(self, data):
		f = open('cache.db','r')
		existing = pickle.load(f)
		f.close()
		dontupdate = 0
		if data in existing:
			dontupdate = 1

		if dontupdate == 0:
			existing.append(data)
			f = open('cache.db','w')
			pickle.dump(existing, f)
			f.close()

	def read(self,artist, title):
		f = open('cache.db','r')
		database = pickle.load(f)
		f.close()
		dic = 0
		for item in database:
			if item['Artist'] == artist and item['Title'] == title:
				dic = item
		if dic != 0:
			dic['Cached'] = True
		return dic
