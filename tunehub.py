#!/usr/bin/python2

import sys
import traceback
import threading
import urllib, urllib2
#Custom Traceback Handler
def errorhandler(type, value, tb):
    print '\n========TuneHub Error Handler========'
    print 'TuneHub just crashed. Informations about this crash :'
    traceback.print_exception(type, value, tb)
    f = open('error.log', 'a')
    traceback.print_exception(type, value, tb, limit = None, file = f)
    print '\nError Information has been written in error.log'
    print 'Next time you launch TuneHub, it will send us the bug report.'
    print '==========Tips==========\nOne TuneHub\'s common cause of crash is data corruption.\nRemove cache.db and meta.db files and try again.'
sys.excepthook = errorhandler
#End of handler

sys.path.append('modules/')
sys.path.append('lib/')
sys.path.append('modules/sites')

tkready = True
try:
    import Tkinter, tkFileDialog
except:
    tkready = False

from windows import Windows
import pickle
import filehandler, id3handler
import os
import time
from cache import Cache
import lyricsapi2
from datastruct import Structure
from tagexporter import TagExport
from txtexporter import TxtExport
import progressbar

win = Windows(title = 'TuneHub CLI')
win.begin()

print "TuneHub - Lyrics Fetching Made Easy\nCopyright 2011 Hugo Caille under the GNU GPL v3 license.\n==> This is a developpement version, don't except it to works perfectly.\n==> Please report bugs and crashes to hugo@gkz.fr.nf\n==> TuneHub will try to report bugs automatically. These reports are anonymous.\n"

#Error Sending System
def bugreport():
    f = open('error.log')
    data = f.read()
    f.close()
    postdata = {'bug' : data}
    postdata = urllib.urlencode(postdata)
    request = urllib2.Request('http://www.tunehub.tk/bugreport.php', postdata)
    try:
	page = urllib2.urlopen(request)
	page.close()
	os.remove('error.log')
	print 'Report succesfully sent. Thank you for testing TuneHub :)'
    except urllib2.HTTPError:
	print 'Unable to send the bug report.'

    print 'Press Enter'
if os.path.isfile('error.log'):
    print 'A crashed occured last time you used TuneHub.\nSending crash informations in background...\n'
    bugthread = threading.Thread(group=None, target=bugreport)
    bugthread.start()
    

def metadata():
	global tkready
	def musicPath():
	    global tkready
	    path = None
	    if tkready == True:
		print 'Please pick up a file in the path selection window'
		global tkroot
		tkroot = Tkinter.Tk()
		
		path = tkFileDialog.askdirectory(parent=tkroot,title="Please select your music path")
		tkroot.destroy()
		print 'Choosed path: ' + path
		if len(path)<2:
		    path = None
	    if path == None or tkready == False:
		if tkready == True:
		    print 'You haven\'t provide the path through the Graphical Interface. Please follow this'
		print "Now enter your music (or player) path"
		print 'Examples : H: on Windows or /media/myPlayer on UNIX (Linux, Mac OS X, BSD and Others...)'
		path = raw_input('Path: ')
	    return path
	path = musicPath()
	if len(path)==0:
		print "You haven't provide your music path. Program will now exit"
		sys.exit()
	print '\nMetadata database have meta.db as default name. If you wanna change this, type the new name now'
	output = raw_input("Metadata database's name: ")
	if len(output) == 0:
		output = 'meta.db'
	print '\n'
	
	import pickle
	print 'The scan can take few minutes, depending on your drive size'
	import filehandler
	Filer = filehandler.Filer(path)

	import id3handler
	print "Listing Music directory..."
	mp3list = Filer.supportedList()
	total = str(len(mp3list))
	print total + ' tracks have been found'

	metalist = []
	print "Collecting metadata from ID3 tags..."
	for item in mp3list:
		
		id3 = id3handler.ID3handler(filename=item)
		info = data = id3.get()
		
		if info != 0:
			metalist.append(info)
	total = str(len(metalist))
	print total + ' tags have been parsed'
	print "Writing database...",
	f=open(output,'w')
	pickle.dump(metalist, f)
	f.close()
	print "[ DONE ]"
        
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

def tagexport():
    print 'Opening lyrics.db...',
    f = open('lyrics.db')
    data = pickle.load(f)
    f.close()
    print '[ DONE ]'
    datalen = len(data)
    from tagexporter import TagExport
    widgets = ['Exporting: ', progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker()), ' ', progressbar.ETA()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=datalen).start()
    count = 0
    for item in data:
	count = count + 1
	pbar.update(count)
        motor = TagExport(item)
        motor.make()
    pbar.finish()
    print 'Lyrics have been exported in their respective files tags'

def txtexport():
    print 'Opening lyrics.db...',
    f = open('lyrics.db')
    data = pickle.load(f)
    f.close()
    print '[ DONE ]'
    
    from txtexporter import TxtExport
    print 'Exporting...',
    for item in data:
        motor = TxtExport(item)
        motor.make()
    print '[ DONE ]'
    print 'Lyrics have been exported in the export/ directory'


while 1:
    try:
        cmd = raw_input('TuneHub> ')
    except KeyboardInterrupt:
        print '\n'
        exit()
        
    if len(cmd) < 1 :
        print "Type 'help' for a list of available commands."
        
    if cmd == 'help':
        print '==>List of available commands'
        print '>help: Show the list of commands'
        print '>scan: Search a directory for music.'
        print '>fetch: Fetch the songs lyrics on the Internet.'
        print '>export: Export the lyrics as .txt files'
        print '>tag: Export fetched lyrics in the music files ID3 tags'
        print '>exit: Exit TuneHub'
    
    if cmd == 'scan':
        metadata()
    
    if cmd == 'fetch':
        lyrics()
    
    if cmd == 'export':
        txtexport()
        
    if cmd == 'tag':
        tagexport()
    
    if cmd == 'exit':
        print '\n'
        exit()
