#!/usr/bin/python
import sys
outencoding = sys.stdout.encoding
sys.path.append('modules/')
sys.path.append('lib/')
sys.path.append('modules/sites')

if __name__ == '__main__':
	from windows import Windows
	win = Windows(title='LyricsFetcher Lyrics Downloader')
	win.begin()

from os.path import isfile

import pickle
import time

from cache import Cache

def lyrics():
	global found
	print 'Reading meta.db...',
	f = open('meta.db','r')
	meta = pickle.load(f)
	f.close()
	total = len(meta)
	print str(total) + ' songs found.'
	
	import lyricsapi2
	found = []
	notfound = []
	
	from datastruct import Structure
	
	def save():
		global found
		f=open('lyrics.db','w')
		pickle.dump(found,f)
		f.close()
	
	
	done = 0
	elapsedtime = 0
	
	foundcount = 0
	notfoundcount = 0
	
	cacheobject = Cache()
	
	for item in  meta:
		try:
			beginningtime = time.time()
			structAPI = Structure(item)
			artist = structAPI.Artist()
			title = structAPI.Title()
			album = structAPI.Album()
			year = structAPI.Year()
			try:
				print 'Getting lyrics for ' + artist.encode(outencoding) + ' - ' + title.encode(outencoding)
			except:
				print 'Getting lyrics for ' + repr(artist) + ' - ' + repr(title)
			Lyricsapi = lyricsapi2.Lyrics(cacheobject, artist, title, album, year)
			
			fetched = Lyricsapi.get()
			if fetched != 0:
				fetched['Filename'] = item['Filename']
				found.append(fetched)
				save()
			
			structAPI = Structure(fetched)
			lyric = structAPI.Lyric()
			cached = structAPI.Cached()
			if lyric != None:
				foundcount = foundcount + 1
				if cached == True:
					print ">>> Found (Cached)"
				else:
					print ">>> Found"
			else:
				notfoundcount = notfoundcount + 1
				if cached == True:
					print "!!! Not Found (Cached)"
				else:
					print "!!! Not Found"
			
			endtime = time.time()
			loopduration = endtime - beginningtime
			elapsedtime = elapsedtime + loopduration
			done = done +1
			eta = ((total * elapsedtime)/done) - elapsedtime
			percentage = (done*100)/total
			foundpercentage = (foundcount*100)/total
			notfoundpercentage = (notfoundcount*100)/total
			print str(foundcount)  + ' lyrics found (' + str(foundpercentage) + '%). ' + str(notfoundcount) + ' not found (' + str(notfoundpercentage) + '%). ' + str(foundcount+notfoundcount) + '/' + str(total)
			elapsedtuple = time.gmtime(elapsedtime)
			timeformat = '%H:%M:%S'
			elapsedstr = time.strftime(timeformat, elapsedtuple)
			etatuple = time.gmtime(eta)
			etastr = time.strftime(timeformat, etatuple)
			print str(percentage) + '%  ' + elapsedstr + '  elapsed. Remaining time: ' + etastr + '\n'
		
		except KeyboardInterrupt:
			sys.exit()

if __name__ == '__main__':
	lyrics()	
	win.end()