#!/usr/bin/python
'''TuneHub CLI.
    Copyright (C) 2011  Hugo Caille

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

#Python level-1 imports
import sys
import os
import traceback
#Custom Traceback Handler
def errorhandler(type, value, tb):
    print '\n========TuneHub Error Handler========'
    print 'TuneHub just crashed. Informations about this crash :'
    traceback.print_exception(type, value, tb)
    f = open('error.log', 'a')
    traceback.print_exception(type, value, tb, limit = None, file = f)
    print '\nError Information has been written in error.log'
    print 'Next time you launch TuneHub, it will send us the bug report.'
    if os.name == 'nt':
	print 'Press enter to quit'
	raw_input()
	
sys.excepthook = errorhandler
#End of Custom Traceback Handler

#Python level-2 imports
import threading, urllib, urllib2, pickle, time, logging

#Optionnal Tkinter library import
tkready = True
try:
    import Tkinter, tkFileDialog
except:
    tkready = False
#End of Tkinter import process

#Third-party imports
import progressbar

#TuneHub internal modules imports.
import tunehubcore
from tunehubcore import windows, filehandler, id3handler, cache, lyricsapi2, datastruct, tagexporter, txtexporter

#Initialising Windows-specific environnement.
win = windows.Windows(title = 'TuneHub CLI')
win.begin()

#Initialising locales
import gettext
import locale

def init_localization():
  '''prepare l10n'''
  locale.setlocale(locale.LC_ALL, '') # use user's preferred locale
  # take first two characters of country code
  loc = locale.getlocale()
  
  if win.isWindows():
    filename = "res/windows/messages_%s.mo" % locale.getlocale()[0][0:2]
  else:
    filename = "res/messages_%s.mo" % locale.getlocale()[0][0:2]

  try:
    logging.debug( "Opening message file %s for locale %s", filename, loc[0] )
    trans = gettext.GNUTranslations(open( filename, "rb" ) )
  except IOError:
    logging.debug( "Locale not found. Using default messages" )
    trans = gettext.NullTranslations()

  trans.install()

if __name__ == '__main__':
  init_localization()

#Greeting Message
print "TuneHub - Lyrics Fetching Made Easy"
print "Copyright (C) 2011  Hugo Caille\n\n==> This program comes with ABSOLUTELY NO WARRANTY.\n==> This is free software, and you are welcome to redistribute it\n==> under certain conditions. For details, read the COPYING file\n==> or visit http://www.gnu.org/licenses/gpl-3.0.txt\n"

#Checks cache.db, meta.db and lyrics.db for corruption. They will be deleted if they can't be open by Pickle.
def fileCheck(filename):
    if os.path.isfile(filename):
	f = open(filename, 'r')
	try:
	    pickle.load(f)
	except:
	    os.remove(filename)
	    print _('%s was corrupted. Now deleted to prevent file corruption issues.') %filename
fileCheck('meta.db')
fileCheck('cache.db')
fileCheck('lyrics.db')
#End of filecheck.

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
	print _('Report succesfully sent. Thank you for testing TuneHub :)')
    except urllib2.HTTPError:
	print _('Unable to send the bug report.')

    print _('Press Enter')
if os.path.isfile('error.log'):
    print _('A crashed occured last time you used TuneHub.\nSending crash informations in background...\n')
    bugthread = threading.Thread(group=None, target=bugreport)
    bugthread.start()
#End of the error seding system.
    

def metadata():
#Scans a path for metadata, fills-in meta.db
	global tkready
	def musicPath():
	    global tkready
	    path = None
	    if tkready == True:
		print _('Please pick up a file in the path selection window')
		global tkroot
		tkroot = Tkinter.Tk()
		
		path = tkFileDialog.askdirectory(parent=tkroot,title=_("Please select your music path"))
		tkroot.destroy()
		print _('Choosed path: %s') %path
		if len(path)<2:
		    path = None
	    if path == None or tkready == False:
		if tkready == True:
		    print _('You haven\'t provide the path through the Graphical Interface. Please follow this')
		print _("Now enter your music (or player) path")
		print _('Examples : H: on Windows or /media/myPlayer on UNIX (Linux, Mac OS X, BSD and Others...)')
		path = raw_input(_('Path: '))
	    return path
	path = musicPath()
	if len(path)==0:
		print _("You haven't provide your music path. Program will now exit")
		sys.exit()
	print _('\nMetadata database have meta.db as default name. If you wanna change this, type the new name now')
	output = raw_input( _("Metadata database's name: ") )
	if len(output) == 0:
		output = 'meta.db'
	print '\n'
	print _('The scan can take few minutes, depending on your drive size')
	Filer = filehandler.Filer(path)
	print _("Listing Music directory...")
	mp3list = Filer.supportedList()
	total = str(len(mp3list))
	print _('%s tracks have been found') %total

	metalist = []
	print _("Collecting metadata from ID3 tags...")
	for item in mp3list:
		
		id3 = id3handler.ID3handler(filename=item)
		info = data = id3.get()
		
		if info != 0:
			metalist.append(info)
	total = str(len(metalist))
	print _('%s tags have been parsed') %total
	print _("Writing database..."),
	f=open(output,'w')
	pickle.dump(metalist, f)
	f.close()
	print _("[ DONE ]")

        
def lyrics():
#Fetch the lyrics on Internet.
	global found
	print _('Reading meta.db...'),
	f = open('meta.db','r')
	meta = pickle.load(f)
	f.close()
	total = len(meta)
	print _('%s songs found.') %total
	
	found = []
	notfound = []
	
	Structure = datastruct.Structure
	
	def save():
		global found
		f=open('lyrics.db','w')
		pickle.dump(found,f)
		f.close()
	
	
	done = 0
	elapsedtime = 0
	
	foundcount = 0
	notfoundcount = 0
	
	cacheobject = cache.Cache()
	
	for item in  meta:
		try:
			beginningtime = time.time()
			structAPI = Structure(item)
			artist = structAPI.Artist()
			title = structAPI.Title()
			album = structAPI.Album()
			year = structAPI.Year()
			try:
				print _('Getting lyrics for {0} - {1}').format(artist.encode(outencoding), title.encode(outencoding))
			except:
				print _('Getting lyrics for {0} - {1}').format(repr(artist), repr(title))
			Lyricsapi = lyricsapi2.Lyrics(cacheobject, artist, title, album, year)
			
			fetched = Lyricsapi.get()
			if fetched != 0:
				fetched['Filename'] = item['Filename']
				found.append(fetched)
				save()
			
			structAPI = datastruct.Structure(fetched)
			lyric = structAPI.Lyric()
			cached = structAPI.Cached()
			if lyric != None and lyric != 'Error':
				foundcount = foundcount + 1
				if cached == True:
					print _(">>> Found (Cached)")
				else:
					print _(">>> Found")
			else:
				notfoundcount = notfoundcount + 1
				if cached == True:
					print_( "!!! Not Found (Cached)")
				else:
					print _("!!! Not Found")
			
			endtime = time.time()
			loopduration = endtime - beginningtime
			elapsedtime = elapsedtime + loopduration
			done = done +1
			eta = ((total * elapsedtime)/done) - elapsedtime
			percentage = (done*100)/total
			foundpercentage = (foundcount*100)/total
			notfoundpercentage = (notfoundcount*100)/total
			print _('{0} lyrics found ({1}%). {2} not found ({3}%). {4}/{5}  ').format( str(foundcount), str(foundpercentage), str(notfoundcount), str(notfoundpercentage), str(foundcount + notfoundcount), str(total) )
			#print str(foundcount)  + ' lyrics found (' + str(foundpercentage) + '%). ' + str(notfoundcount) + ' not found (' + str(notfoundpercentage) + '%). ' + str(foundcount+notfoundcount) + '/' + str(total)
			elapsedtuple = time.gmtime(elapsedtime)
			timeformat = '%H:%M:%S'
			elapsedstr = time.strftime(timeformat, elapsedtuple)
			etatuple = time.gmtime(eta)
			etastr = time.strftime(timeformat, etatuple)
			print _('{0}%  {1}  elapsed. Remaining time: {2}\n').format( str(percentage), elapsedstr, etastr)
			#print str(percentage) + '%  ' + elapsedstr + '  elapsed. Remaining time: ' + etastr + '\n'
		
		except KeyboardInterrupt:
			sys.exit()

def tagexport():
#Exports the lyrics in music tags
    print _('Opening lyrics.db...'),
    f = open('lyrics.db')
    data = pickle.load(f)
    f.close()
    print _('[ DONE ]')
    datalen = len(data)
    widgets = [_('Exporting: '), progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker()), ' ', progressbar.ETA()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=datalen).start()
    count = 0
    for item in data:
	count = count + 1
	pbar.update(count)
        motor = tagexporter.TagExport(item)
        motor.make()
    pbar.finish()
    print _('Lyrics have been exported in their respective files tags')

def export(mode='export'):
#Exports the lyrics as txt in export/ path or in the same paths as audio files.
    print _('Opening lyrics.db...'),
    f = open('lyrics.db')
    data = pickle.load(f)
    f.close()
    print _('[ DONE ]')

    print _('Exporting...'),
    for item in data:
        motor = txtexporter.TxtExport(item, mode)
        motor.make()
    print _('[ DONE ]')
    if mode=='export':
	print _('Lyrics have been exported in the export/ directory')
    if mode=='path':
	print _('Lyrics have been exported in corresponding songs directories')

#CLI loop
while 1:
    try:
        cmd = raw_input('TuneHub> ')
    except KeyboardInterrupt:
        print '\n'
        exit()
        
    if len(cmd) < 1 :
        print _("Type 'help' for a list of available commands.")
        
    if cmd == 'help':
        print _('==>List of available commands')
        print _('>help: Show the list of commands')
        print _('>scan: Search a directory for music.')
        print _('>fetch: Fetch the songs lyrics on the Internet.')
        print _('>export: Export the lyrics as .txt files in export/')
	print _('>txt: Export the lyrics as .txt in the songs directories.')
        print _('>tag: Export fetched lyrics in the music files ID3 tags')
        print _('>exit: Exit TuneHub')
    
    if cmd == 'scan':
        metadata()
    
    if cmd == 'fetch':
        lyrics()
    
    if cmd == 'export':
        export()
	
    if cmd == 'txt':
	export('path')
        
    if cmd == 'tag':
        tagexport()
    
    if cmd == 'exit':
        print '\n'
        exit()
