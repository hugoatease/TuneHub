#!/usr/bin/python
import gpod
import pickle
import sys
sys.path.append('modules/')
import datastruct
import os

ipod = raw_input('iPod Mountpoint: ')
print 'Opening your iPod\'s database...'
itdb = gpod.itdb_parse(ipod, None)

print 'Opening lyrics.db...'
f = open('lyrics.db','r')
data = pickle.load(f)
f.close()

print 'Collecting filenames in lyrics.db...'
filelist = []
for item in data:
    api = datastruct.Structure(item)
    filename = api.Filename()
    lyric = api.Lyric()
    if lyric != None and lyric != 'Error':
        filelist.append(filename)

print 'Alter values...'
for track in gpod.sw_get_tracks(itdb):
    name = track.ipod_path
    name = name.replace(':', '/')
    
    filename = ipod + name
        
    if filename in filelist:
        print filename
        track.lyrics_flag=1
    
print 'Saving in local file iTunesDB'
gpod.itdb_write_file(itdb, 'iTunesDB', None)
