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