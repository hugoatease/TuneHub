from TextInformationFrame import *
class artistFrame(TextInformationFrame):
    def __init__(self):
        self.artist = ''
        TextInformationFrame.__init__(self)

    def decode(self, data):
        self.artist = TextInformationFrame.decode(self, data)

    def encode(self):
        return TextInformationFrame.encode(self)

    def pack(self, frameDict):
        return TextInformationFrame.pack(self, frameDict)

    def unpack(self):
        return TextInformationFrame.unpack(self, 'Lead Performer(s)/Soloist(s)')
