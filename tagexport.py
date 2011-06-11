#!/usr/bin/python
import sys
sys.path.append("modules/")

if __name__ == '__main__':
    from windows import Windows
    win = Windows(title = 'LyricsFetcher Exporter')
    win.begin()
import pickle

def tagexport():
    print 'Opening lyrics.db...',
    f = open('lyrics.db')
    data = pickle.load(f)
    f.close()
    print '[ DONE ]'
    
    from tagexporter import TagExport
    print 'Exporting...',
    for item in data:
        motor = TagExport(item)
        motor.make()
    print '[ DONE ]'
    print 'Lyrics have been exported in their respective files tags'

if __name__ == '__main__':
    tagexport()
    win.end()