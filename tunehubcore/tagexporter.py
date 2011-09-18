'''TuneHub Core Library.
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

from tunehubcore import id3handler
from tunehubcore import datastruct
from filter import LyricsFilter

class TagExport:
    def __init__(self, item):
        structAPI = datastruct.Structure(item)
        self.filename = structAPI.Filename()
        self.lyric = structAPI.Lyric()
    
    def write(self):
        motor = id3handler.ID3handler(self.filename)
        try:
            motor.writeLyrics(self.lyric)
        except IOError:
            print '!!! Unable to write Lyrics for ' + self.filename

    def make(self):
        if self.lyric != None and len(self.filename)>1:
            status = self.filter()
            if status == False:
                self.write()
    
    def filter(self):
        api = LyricsFilter(self.lyric)
        status = api.get()
        return status