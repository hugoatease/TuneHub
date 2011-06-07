#!/usr/bin/python
import sys
sys.path.append("modules/")

if __name__ == '__main__':
    from windows import Windows
    win = Windows(title = 'LyricsFetcher Exporter')
    win.begin()
import pickle

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

if __name__ == '__main__':
    txtexport()
    win.end()