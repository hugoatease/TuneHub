
class LyricsFilter:
    
    def __init__(self, lyric):
        self.lyric = lyric
        self.result = False
        
    def instrumental(self):
        contain = False
        lines = self.lyric.count('\n')
        lyric = self.lyric.lower()
        
        if 'instrumental' in lyric:
            contain = True
            
        if contain == True and lines < 5:
            self.result = True
            
    def html(self):
        leftcount = self.lyric.count('<')
        rightcount = self.lyric.count('>')
        count = int( (leftcount + rightcount)/2 )
        
        if count > 4:
            self.result = True
            
    def get(self):
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