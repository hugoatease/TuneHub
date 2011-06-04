import sys
sys.path.append('modules/')
sys.path.append('lib/')
sys.path.append('modules/sites')
from os.path import isfile

import pickle

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

import progressbar
widgets = ['Downloading: ', progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker()),' ', progressbar.ETA()]
#pbar = progressbar.ProgressBar(widgets=widgets, maxval=total).start()

bari=0

for item in  meta:
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
	bari = bari +1
	structAPI = Structure(fetched)
	lyric = structAPI.Lyric()
	if lyric != None:
		cached = structAPI.Cached()
		if cached == True:
			print ">>> Found (Cached)"
		else:
			print ">>> Found"
	else:
		print "!!! Not Found"
	#pbar.update(bari)
#pbar.finish()
