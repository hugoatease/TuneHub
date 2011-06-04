from InvalidFrameError import *
from array import *

class TextInformationFrame:
	    """Class to represent ID3v2 Text Information frames
    Please extend this class rather than using it directly"""

    def __init__(self):
        """Initializer. Called by subclasses."""
        self.preserveIfTagAltered = 1
        self.preserveIfFileAltered = 1
        self.readOnly = 0
        self.compressed = 0
        self.encrypted = 0
        self.groupInformation = 0
        self.encoding = 'ISO-8859-1'
        self.tag = ''

    def __cmp__(self, other):
        """Comparison method. If the tag, flags, encoding and text are the same, it's the same flag."""
        if self.tag == other.tag and \
           self.preserveIfTagAltered == other.preserveIfTagAltered and \
           self.preserveIfFileAltered == other.preserveIfFileAltered and \
           self.readOnly == other.readOnly and \
           self.compressed == other.compressed and \
           self.encrypted == other.encrypted and \
           self.groupInformation == other.groupInformation and \
           self.encoding == other.encoding and \
           self.text == other.text:
	            return 0
        else:
	            return 1

    def getFrameID(self):
        """Most text Information frames are only supposed to be present once in a tag. Therefore,
        the tag is the frame ID."""
        return self.tag

    def decode(self, data):
        """Given a byte array assumed to represent a Comment object, this method constructs the comment object"""
        self.tag = data[:4].tostring()
        
        # Cut off tag and length bytes
        data = data[8:]

        # First Flag byte:
        flag = data.pop(0)
        if ord(flag) | ord('\xE0') <> ord('\xE0'):
	            raise InvalidFrameError("ID3v2 reserved flag set")
            return
        if ord(flag) & ord('\x80') == ord('\x80'):
	            self.preserveIfTagAltered = 1
        if ord(flag) & ord('\x40') == ord('\x40'):
	            self.preserveIfFileAltered = 1
        if ord(flag) & ord('\x20') == ord('\x20'):
	            self.readOnly = 1

        # Second Flag byte:
        flag = data.pop(0)
        if ord(flag) | ord('\xE0') <> ord('\xE0'):
	            raise InvalidFrameError("ID3v2 reserved flag set")
            return
        if ord(flag) & ord('\x80') == ord('\x80'):
	            self.compressed = 1
        if ord(flag) & ord('\x40') == ord('\x40'):
	            self.encrypted = 1
        if ord(flag) & ord('\x20') == ord('\x20'):
	            self.groupInformation = 1 # Who am I kidding? No support for this.

        #Its either 0 for ISO-8859-1, or 1 for Unicode
        encoding = data.pop(0)
        if encoding == '\x00':
	            self.encoding = 'ISO-8859-1'
        elif encoding == '\x01':
	            self.encoding = 'UTF-16'
        elif encoding == '\x02':
	            self.encoding = 'UTF-16BE'
        elif encoding == '\x03':
	            self.encoding = 'UTF-8'
        

        if not self.compressed:
	            if not self.encrypted:
		                if self.encoding == 'ISO-8859-1':
			                    self.text = data.tostring()
                    return self.text
                else:
	                    raise InvalidFrameError("Unsupported encoding")
                    return
            else:
	                raise InvalidFrameError("Encrypted Frame - Unsupported")
                return
        else:
	            raise InvalidFrameError("Compressed Frame - Unsupported")
            return

    def encode(self):
	        """The opposite of decode, this object constructs a properly formatted ID3v2 frame from an object."""
        frame = array('B')
        frame.fromstring(self.tag)
        length = len(self.text) + 1 # add one byte for 'encoding'
        
        for i in range(4):
	            if length >= pow(256, (3-i)):
		                frame.append((length - (length % pow(256,(3-i)))) / pow(128,(3-i)))
                length = pow(256,(3-i)) % length
            elif length < pow(256, (3-i)):
	                frame.append(ord('\x00'))

        flag = '\x00'
        if self.preserveIfTagAltered:
	            flag = chr(ord(flag) | ord('\x80'))
        if self.preserveIfFileAltered:
	            flag = chr(ord(flag) | ord('\x40'))
        if self.readOnly:
	            flag = chr(ord(flag) | ord('\x20'))
        frame.append(ord(flag))

        flag = '\x00'
        if self.compressed:
	            flag = chr(ord(flag) | ord('\x80'))
        if self.encrypted:
	            flag = chr(ord(flag) | ord('\x40'))
        if self.groupInformation:
	            flag = chr(ord(flag) | ord('\x20'))
        frame.append(ord(flag))

        if self.encoding == 'ISO-8859-1':
	            frame.append(ord('\x00'))
        else:
	            frame.append(ord('\x01')) #Not supporting unicode yet  
            
        frame.fromstring(self.text) #

        return frame

    def pack(self, frameDict):
	        """Given a dictionary of the tag and text, this method creates the object."""
        self.tag = frameDict['TAG']
        self.text = frameDict['text']
        if frameDict.has_key('flags'):
	            if len(frameDict['flags']) == 16:
		                self.preserveIfTagAltered = frameDict['flags'].pop(0)
                self.preserveIfFileAltered = frameDict['flags'].pop(1)
                self.readOnly = frameDict['flags'].pop(2)
                self.compressed = frameDict['flags'].pop(8)
                self.encrypted = frameDict['flags'].pop(9)
                self.groupInformation = frameDict['flags'].pop(10)

                #These next lines only work if the Pop trick above worked.
                if frameDict['flags'].index('1') >= 0:
	                    raise InvalidFrameError("Undefined flag set in %s" % (tag))

    def unpack(self, description):
	        """A debugging method, this returns a dictionary representing the object in string form."""
        flags = ''
        if self.preserveIfTagAltered:
	            flags = 'preserveIfTagAltered:'
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
        return {'TAG':self.tag, 'Description':description,
                'Length':str(len(self.text)+1), 'Flags':flags,
                'Encoding':self.encoding, 'Text':self.text}
