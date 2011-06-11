#!/usr/bin/python
import gpod
ipodpath = raw_input('iPod Mountpoint: ')
print 'Opening your iPod\'s database...'
itdb = gpod.itdb_parse(ipodpath, None)

print 'Alter values...'
for track in gpod.sw_get_tracks(itdb):
    track.lyrics_flag=1
    
print 'Saving in local file itunes.db...'
gpod.itdb_write_file(itdb, 'itunes.db', None)
