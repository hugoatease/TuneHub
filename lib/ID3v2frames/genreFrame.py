from TextInformationFrame import *
class genreFrame(TextInformationFrame):
    def __init(self):
        self.genre = ''
        TextInformationFrame.__init__(self)

    def decode(self, data):
        self.genre = TextInformationFrame.decode(self, data)

    def encode(self):
        return TextInformationFrame.encode(self)

    def pack(self, frameDict):
        return TextInformationFrame.pack(self, frameDict)

    def unpack(self):
        return TextInformationFrame.unpack(self, 'Content Type')
