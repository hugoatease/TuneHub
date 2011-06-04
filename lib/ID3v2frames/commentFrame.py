from array import *

class commentFrame:
    """Class to represent ID3v2 comment frames"""
    def __init__(self, language='eng', description='COMMENT', comment=''):
        """Initializer. Can accept the language, description and Comment, the three things required for 
        a unique Comment frame."""
        self.encoding = 'ISO-8859-1'
        self.language = language
        self.description = description
        self.comment = comment
        self.preserveIfTagAltered = 1
        self.preserveIfFileAltered = 1
        self.readOnly = 0
        self.compressed = 0
        self.encrypted = 0
        self.groupInformation = 0

    def __cmp__(self, other):
        """Comparison method. If the Tag, flags, language, description and comment are the same, this 
        is the same comment. The specification says so, so don't blame me."""
        if self.tag == other.tag and \
           self.preserveIfTagAltered == other.preserveIfTagAltered and \
           self.preserveIfFileAltered == other.preserveIfFileAltered and \
           self.readOnly == other.readOnly and \
           self.compressed == other.compressed and \
           self.encrypted == other.encrypted and \
           self.groupInformation == other.groupInformation and \
           self.encoding == other.encoding and \
           self.language == other.language and \
           self.description == other.description and \
           self.comment == other.comment:
            return 0
        else:
            return 1

    def getFrameID(self):
        """Returns an identifier suitable to identify the critical portions of a comment which makes it
        unique. Used to identify the comment in the tag's internal frame dictionary."""
        return 'COMM'+self.language+self.description
        

    def decode(self, data):
        """Given a byte array assumed to represent a Comment object, this method constructs the comment object"""
        #Strip off Tag and Length. We don't need them
        data = data[8:]

        flag = data.pop(0)
        if ord(flag) | ord('\xE0') <> ord('\xE0'):
            raise InvalidTagError("ID3v2 reserved flag set")
            return
        if ord(flag) & ord('\x80') == ord('\x80'):
            self.preserveIfTagAltered = 1
        if ord(flag) & ord('\x40') == ord('\x40'):
            self.preserveIfFileAltered = 1
        if ord(flag) & ord('\x20') == ord('\x20'):
            self.readOnly = 1

        flag = data.pop(0)
        if ord(flag) | ord('\xE0') <> ord('\xE0'):
            raise InvalidTagError("ID3v2 reserved flag set")
            return
        if ord(flag) & ord('\x80') == ord('\x80'):
            self.compressed = 1
        if ord(flag) & ord('\x40') == ord('\x40'):
            self.encrypted = 1
        if ord(flag) & ord('\x20') == ord('\x20'):
            self.groupInformation = 1 # Who am I kidding? No support for this.

        self.encoding = data.pop(0)

        self.language = data[:3].tostring()

        data = data[3:]

        if not self.compressed:
            if not self.encrypted:
                if ord(self.encoding) == 0: # No Unicode, yet
                    self.encoding = 'ISO-8859-1'
                    self.description = data[:data.index('\x00')].tostring()
                    self.comment = data[data.index('\x00'):].tostring()
                else:
                    raise InvalidTagError("Unsupported encoding")
                    return
            else:
                raise InvalidTagError("Encrypted Frame")
                return
        else:
            raise InvalidTagError("Compressed Frame")
            return

    def encode(self):
        """The opposite of decode, this object constructs a properly formatted ID3v2 frame from an object."""
        frame = array('B')
        frame.fromstring('COMM')
        length = len(self.description) + len(self.comment) + 5 # add one byte for 'encoding'
        
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
            flag = chr(ord(flag) | ord('\x40'))
        frame.append(ord(flag))

        flag = '\x00'
        if self.compressed:
            flag = chr(ord(flag) | ord('\x40'))
        if self.encrypted:
            flag = chr(ord(flag) | ord('\x40'))
        if self.groupInformation:
            flag = chr(ord(flag) | ord('\x40'))
        frame.append(ord(flag))

        if self.encoding == 'ISO-8859-1':
            frame.append(ord('\x00'))
        else:
            frame.append('\x01') #Not supporting unicode yet  
            
        frame.fromstring(self.language)
        frame.fromstring(self.description)
        frame.append(ord('\x00'))
        frame.fromstring(self.comment)


        return frame

    def pack(self, frameDict):
        """Given a dictionary of the tag, language, description and format, this method creates the object."""
        self.tag = 'COMM'
        self.language = frameDict['language']
        self.description = frameDict['description']
        self.comment = frameDict['comment']
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

    def unpack(self):
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
        return {'TAG':'COMM', 'Frame Description':'Comments',
                'Length':str(len(self.description)+len(self.comment)+5),
                'Flags':flags, 'Encoding':self.encoding, 'Language':self.language,
                'Description':self.description, 'Comment':self.comment}
