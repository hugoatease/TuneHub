import sys
sys.path.append('modules/')
sys.path.append('lib/')

from os.path import isfile

import pickle

print 'Reading meta.db...',
f = open('meta.db','r')
meta = pickle.load(f)
f.close()
total = len(meta)
print str(total) + ' songs found.'

import lyricsapi
found = []
notfound = []


def save():
	global found
	f=open('lyrics.db','w')
	pickle.dump(found,f)
	f.close()

import progressbar
widgets = ['Downloading: ', progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker()),' ', progressbar.ETA()]
pbar = progressbar.ProgressBar(widgets=widgets, maxval=total).start()

bari=0
for item in  meta:
	Lyricsapi = lyricsapi.Lyrics(artist=item['Artist'], title=item['Name'])
	fetched = Lyricsapi.getLyric()

	if fetched != 0:
		fetched['File'] = item['File']
		found.append(fetched)
		save()
	bari = bari +1
	pbar.update(bari)
pbar.finish()
print str(bari) + ' lyrics found'
