import sys
sys.path.append('modules/')
def metadata(path,output):

	import pickle

	import filer
	Filer = filer.Filer(path)

	import id3handler
	print "Listing Music directory...",
	mp3list = Filer.mp3list()
	total = str(len(mp3list))
	print total + ' tracks have been found'

	metalist = []
	print "Collect metadata from working ID3v2 tags...",
	for i in mp3list:
		item = mp3list[i]
		id3 = id3handler.ID3handler(filename=item)
		info = data = id3.basicInfov2()
	
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
print 'Now gimme your iPod path, for e.g /media/iPod/, WITH THE TRAILING \'/\' '
path = raw_input('iPod path: ')
if len(path)==0:
	print "You haven't provide your iPod's path. Program will now exit"
	sys.exit()
print '\nMetadata database have meta.db as default name. If you wanna change this, type the new name now'
output = raw_input("Metadata database's name: ")
if len(output) == 0:
	output = 'meta.db'
print '\n'
metadata(path, output)

