#!/usr/bin/python
import sys
sys.path.append("modules/")
from windows import Windows
win = Windows(title = 'LyricsFetcher Exporter')
win.begin()
import pickle

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

win.end()