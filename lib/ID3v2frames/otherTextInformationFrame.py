from TextInformationFrame import *
from id3TagsDict import *

class otherTextInformationFrame(TextInformationFrame):
   def __init__(self):
       self.title = ''
       TextInformationFrame.__init__(self)

   def decode(self, data):
       self.title = TextInformationFrame.decode(self, data)

   def encode(self):
       return TextInformationFrame.encode(self)

   def pack(self, frameDict):
       return TextInformationFrame.pack(self, frameDict)

   def unpack(self):
       return TextInformationFrame.unpack(self,otherTextInformationFrames[self.tag])
