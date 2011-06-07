#!/usr/bin/python

from lyrics import lyrics
from metawalker import metadata
from txtexport import txtexport
import sys

from windows import Windows
win = Windows(title = 'LyricsFetcher Exporter')
win.begin()

print 'Lyrics Fetcher Suite\n(C) Copyright 2011 Hugo Caille under the terms of the GNU GPL v3 license\n'
print 'This software relies on other free and open-source software. For getting the list of these software, type \'thirdparty\'. \n'
print 'For getting the list of commands, type \'help\'. '



while 1:
    try:
        command = raw_input('>>> ')
    except KeyboardInterrupt:
        print '\n'
        sys.exit()
    if command == 'download':
        try:
            lyrics()
        except KeyboardInterrupt:
            print '\n'
    elif command == 'export':
        try:
            txtexport()
        except:
            print '\n'
    elif command == 'scan':
        try:
            metadata()
        except:
            print '\n'
    elif command == 'exit':
        sys.exit()
    elif command == 'help':
        print '> scan: allows you to search a portable music player or a path for MP3s. It builds a meta.db file'
        print '> download: allows you to download lyrics associated with meta.db'
        print '> export: allows you to create an \'export\' directory which contains lyrics ready to go on your player.'
        print '> help: this one. Allows you to getting help, of course'
        print '> thirdparty: Used to show which others programs are included with LyricsFetcher'
        print '> exit: Exit LyricsFetcher'
    else:
        cmdlen = len(command)
        if cmdlen > 0:
            print 'Unknown command. You can get a list of the availaible ones by typing \'help\'. '