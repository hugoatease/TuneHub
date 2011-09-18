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

class LyricsFilter:
    
    def __init__(self, lyric):
        self.lyric = lyric
        self.result = False
        self.dontget = False
        
        if lyric == None:
            self.result = False
            self.dontget = True
        
    def instrumental(self):
        contain = False
        lines = self.lyric.count('\n')
        lyric = self.lyric.lower()
        
        if 'instrumental' in lyric:
            contain = True
            
        if contain == True and lines < 7:
            self.result = True
            
    def html(self):
        leftcount = self.lyric.count('<')
        rightcount = self.lyric.count('>')
        count = int( (leftcount + rightcount)/2 )
        
        if count > 4:
            self.result = True
            
    def get(self):
        if self.dontget == False:
            self.instrumental()
            self.html()
        return self.result
        
if __name__ == '__main__':
    lyric = raw_input('Lyric: ')
    motor = LyricsFilter(lyric)
    status = motor.get()
    print status
    
    if status == True:
        print 'These lyrics have triggered the instrumental or HTML filter'