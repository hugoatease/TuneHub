import sys
sys.path.append('modules/')
sys.path.append('lib/')
sys.path.append('modules/sites')
from os.path import isfile

import pickle
import time

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

for item in  meta:
	beginningtime = time.time()
	structAPI = Structure(item)
	artist = structAPI.Artist()
	title = structAPI.Title()
	print 'Getting lyrics for ' + artist + ' - ' + title
	Lyricsapi = lyricsapi2.Lyrics(artist, title)
	fetched = Lyricsapi.get()

	if fetched != 0:
		fetched['Filename'] = item['Filename']
		found.append(fetched)
		save()
	
	structAPI = Structure(fetched)
	lyric = structAPI.Lyric()
	cached = structAPI.Cached()
	if lyric != None:
		if cached == True:
			print ">>> Found (Cached)"
		else:
			print ">>> Found"
	else:
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
	print str(done) + '/' + str(total) + ' lyrics found. ' + str(percentage) + '%'
	elapsedtuple = time.gmtime(elapsedtime)
	timeformat = '%H:%M:%S'
	elapsedstr = time.strftime(timeformat, elapsedtuple)
	etatuple = time.gmtime(eta)
	etastr = time.strftime(timeformat, etatuple)
	print elapsedstr + '  elapsed. ETA: ' + etastr