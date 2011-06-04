from TextInformationFrame import *
class trackFrame(TextInformationFrame):
    def __init__(self):
        TextInformationFrame.__init__(self)

    def decode(self,data):
        self.track = TextInformationFrame.decode(self, data)

    def encode(self):
        return TextInformationFrame.encode(self)

    def pack(self, frameDict):
        return TextInformationFrame.pack(self, frameDict)

    def unpack(self):
        return TextInformationFrame.unpack(self, 'Track number/Position in set')
