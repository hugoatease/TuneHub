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