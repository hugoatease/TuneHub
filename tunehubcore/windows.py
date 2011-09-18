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

import os

class Windows:
    
    def isWindows(self):
        if os.name == 'nt':
            return True
        else:
            return False
        
    def __init__(self, color='F0',title='LyricsFetcher'):
        iswin = self.isWindows()
        if iswin == True:
            self.windows = True
        else:
            self.windows = False
        
        self.colorname = color
        self.wintitle = title
            
    def color(self):
        if self.windows == True:
            cmd = 'color ' + self.colorname
            os.system(cmd)
            
    def title(self):
        if self.windows == True:
            cmd = 'title ' + self.wintitle
            os.system(cmd)
            
    def pause(self):
        if self.windows == True:
            os.system('pause')
            
    def begin(self):
        self.title()
        self.color()
        
    def end(self):
        self.pause()