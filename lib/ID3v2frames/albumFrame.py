from TextInformationFrame import *
class albumFrame(TextInformationFrame):
    def __init__(self):
        self.album = ''
        TextInformationFrame.__init__(self)

    def decode(self, data):
        self.album = TextInformationFrame.decode(self, data)

    def encode(self):
        return TextInformationFrame.encode(self)

    def pack(self, frameDict):
        return TextInformationFrame.pack(self, frameDict)

    def unpack(self):
        return TextInformationFrame.unpack(self, 'Album/Movie/Show Title')
