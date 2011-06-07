#!/usr/bin/python
import sys
sys.path.append('modules/')
sys.path.append('lib/')
from windows import Windows
win = Windows(title = 'LyricsFetcher Metawalker')
win.begin()

def metadata(path,output):

	import pickle

	import filehandler
	Filer = filehandler.Filer(path)

	import id3handler
	print "Listing Music directory...",
	mp3list = Filer.mp3list()
	total = str(len(mp3list))
	print total + ' tracks have been found'

	metalist = []
	print "Collect metadata from ID3 tags...",
	for item in mp3list:
		
		id3 = id3handler.ID3handler(filename=item)
		info = data = id3.basicInfo()
			
		if info != 0:
			metalist.append(info)
	total = str(len(metalist))
	print total + ' tags have been parsed'
	print "Writing database...",
	f=open(output,'w')
	pickle.dump(metalist, f)
	f.close()
	print "[ DONE ]"

print 'Metadata Finder, a part of the Lyrics Fetcher Suite'
print '(C) Copyright 2011 Hugo Caille. Under the terms of the GNU GPL v3 license\n'
print 'This software uses the ID3v2 tag creation library available at id3v2-py.sf.net under the terms of the GNU GPL license too\n'
print "Now enter your music (or player) path"
print 'Examples : H: on Windows or /media/myPlayer on UNIX (Linux, Mac OS X, BSD and Others...)'
path = raw_input('Path: ')
if len(path)==0:
	print "You haven't provide your music path. Program will now exit"
	sys.exit()
print '\nMetadata database have meta.db as default name. If you wanna change this, type the new name now'
output = raw_input("Metadata database's name: ")
if len(output) == 0:
	output = 'meta.db'
print '\n'
metadata(path, output)

win.end()