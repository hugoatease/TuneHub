from InvalidFrameError import *
from array import *
from md5 import *

class blackBoxFrame:
    """Class to represent ID3v2 unknown data frames"""

    def __init__(self):
        """Initializer. Used primarily to capture tags we just don't know what else to do with."""
        self.preserveIfTagAltered = 0
        self.preserveIfFileAltered = 0
        self.readOnly = 0
        self.compressed = 0
        self.encrypted = 0
        self.groupInformation = 0
        self.tag = ''
        self.data = ''

    def __cmp__(self, other):
        """Comparison function. If the tag, flags and data are the same, it must be the same frame."""
        if self.tag == other.tag and \
           self.preserveIfTagAltered == other.preserveIfTagAltered and \
           self.preserveIfFileAltered == other.preserveIfFileAltered and \
           self.readOnly == other.readOnly and \
           self.compressed == other.compressed and \
           self.encrypted == other.encrypted and \
           self.groupInformation == other.groupInformation and \
           self.encoding == other.encoding and \
           self.data == other.data:
            return 0
        else:
            return 1

    def getFrameID(self):
        """Returns an identifier suitable to identify the critical portions of a comment which makes it
        unique. Used to identify the comment in the tag's internal frame dictionary."""
        #we'll use frameID = tag + md5hash(data). improvements welcome.
        mhash = md5(self.data)
        return self.tag + ":" + mhash.hexdigest()

    def decode(self,data):
        """Given a byte array assumed to represent a Comment object, this method constructs the comment object"""
        self.tag = data[:4].tostring()

        data = data[8:]

        flag = data.pop(0)
        if ord(flag) | ord('\xE0') <> ord('\xE0'):
            raise InvalidFrameError("ID3v2 frame reserved flag set in first flag \
            byte "+str(ord(flag))+" "+self.tag)
        if ord(flag) & ord('\x80') == ord('\x80'):
            self.preserveIfTagAltered = 1
        if ord(flag) & ord('\x40') == ord('\x40'):
            self.preserveIfFileAltered = 1
        if ord(flag) & ord('\x20') == ord('\x20'):
            self.readOnly = 1

        flag = data.pop(0)
        if ord(flag) | ord('\xE0') <> ord('\xE0'):
            raise InvalidFrameError("ID3v2 frame reserved flag set")
        if ord(flag) & ord('\x80') == ord('\x80'):
            self.compressed = 1
        if ord(flag) & ord('\x40') == ord('\x40'):
            self.encrypted = 1
        if ord(flag) & ord('\x20') == ord('\x20'):
            self.groupInformation = 1


        self.data = data


    def encode(self):
        """The opposite of decode, this object constructs a properly formatted ID3v2 frame from an object."""
        frame = array('B')
        frame.fromstring(self.tag)
       
        length = len(self.data)
        for i in range(4):
            if length >= pow(256,(3-i)):
                frame.append((length - (length % pow(256,(3-i)))) / pow(128,(3-i)))
                length = pow(256,(3-i)) % length
            elif length < pow(256,(3-i)):
                frame.append(ord('\x00'))

        flag = 0
        if self.preserveIfTagAltered:
            flag = flag | ord('\x80')
        if self.preserveIfFileAltered:
            flag = flag | ord('\x40')
        if self.readOnly:
            flag = flag | ord('\x20')
        frame.append(flag)

        flag = 0
        if self.compressed:
            flag = flag | ord('\x80')
        if self.encrypted:
            flag = flag | ord('\x40')
        if self.groupInformation:
            flag = flag | ord('\x20')
        frame.append(flag)

        for x in self.data: #TODO-find more efficient way of doing this
            frame.append(ord(x))
            
        return frame

    def unpack(self):
        """A debugging method, this returns a dictionary representing the object in string form."""
        flags = ''
        if self.preserveIfTagAltered:
            flags += 'preserveIfTagAltered:'
        if self.preserveIfFileAltered:
            flags += 'preserveIfFileAltered:'
        if self.readOnly:
            flags += 'readOnly:'
        if self.compressed:
            flags += 'compressed:'
        if self.encrypted:
            flags += 'encrypted:'
        if self.groupInformation:
            flags += 'groupInformation:'

        return {'TAG':self.tag, 'Description':'Unparsed Data',
                'Length':str(len(self.data)), 'Flags':flags}
