from ID3v2frames.titleFrame import *
from ID3v2frames.commentFrame import *
from ID3v2frames.trackFrame import *
from ID3v2frames.genreFrame import *
from ID3v2frames.albumFrame import *
from ID3v2frames.artistFrame import *
from ID3v2frames.blackBoxFrame import *
from ID3v2frames.otherTextInformationFrame import *
from array import *
import string
import os
import ID3v2frames.id3TagsDict

class InvalidTagError:
    """Invalid Tag Error. Raised when something is wrong with the tag. For frame errors,
    an InvalidFrameError is raised"""
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class ID3v2:
    """A Class for manipulating ID3v2 tags."""
    def __init__(self,filename):
        """The Class initializer takes a filename, and parses out the tags.
        It will fail if it encounters an error in the tag flags, or if it encounters a Null frame ID."""
        self.filename = filename
        self.oldHeaderLength = 0
        self.headerArray = array('c')
        
        self.id3v2major = 3
        self.id3v2minor = 0
        self.unsynchronized = 0
        self.extendedHeader = 0
        self.experimentalTag = 0

        self.delete = 0
        self.modified = 0
        self.tagged = 0
        self.frames = {}

        try:
            self.file = open(self.filename, 'r')
            self.file.seek(0)

            #check to see if the file is tagged
            if self.file.read(3) == 'ID3':
                self.tagged = 1
                #check version
                self.id3v2major = ord(self.file.read(1))
                self.id3v2minor = ord(self.file.read(1))

                if self.id3v2major > 3:
                    raise InvalidTagError('ID3v2 major version later than 3')

                #Check the flags
                ID3v2flags = ord(self.file.read(1))
                if ID3v2flags | ord('\xE0') <> ord('\xE0'):
                    raise InvalidTagError('ID3v2 reserved flags set')
                if ID3v2flags & ord('\x80') == ord('\x80'):
                    self.unsynchronized = 1
                if ID3v2flags & ord('\x40') == ord('\x40'):
                    self.extendedHeader = 1
                if ID3v2flags & ord('\x20') == ord('\x20'):
                    self.experimentalTag = 1

                #get the length. It's expressed in 4 bytes of only 7 bits each.
                #lets all pretend its 4 digits of a base 128 number system, shall we?
                tagLength = 0
                for i in range(4):
                    tagLength += (pow(128,(3-i)) * ord(self.file.read(1)))

                #save the length of the old ID3v2 header, we'll need it if we write a new file.
                self.oldHeaderLength = tagLength + 10

                #write the header to an array. It could theoretically be up to 256 MB long,
                #so we might want to figure out a better way to handle it.
                self.headerArray.fromfile(self.file, tagLength)

            else: #we get here if the file doesn't have an ID3 tag
                self.oldHeaderLength = 0

            # Okay, we're done with the old file for now
            self.file.close()
        except IOError, msg:
            raise IOError("Error opening mp3 file: "+ msg)

        #unUnsynchronize if necessary. this function could make bad things happen.
        if self.unsynchronized:
            for i in range(len(self.headerArray)):
                if self.headerArray[i] == '\xFF':
                    if self.headerArray[i+1] == '\x00':
                        self.headerArrary.pop(i+1)
            # All done. lets unset the unsynchronized flag
            self.unsynchronized = 0


        #parse the extended header, if it exists
        if self.extendedHeader:
            #first, get the extended Header Size
            ehSize = 0
            for i in range(4):
                ehSize += (pow(256,(3-1)) * ord(self.headerArray[i]))

            #next, parse the extended header flags
            if self.headerArray[4] == '\x80':
                self.CRCdata = 1
            elif self.headerArray[4] == '\x00':
                self.CRCdata = 0
            else: #bad flag
                raise InvalidTagError('InvalidFlag in Extended Header')
            if self.headerArray[5] <> '\x00':
                raise InvalidTagError('InvalidFlag in Extended Header')

            #finally, grab the padding size. add it to the oldHeaderLength
            #TODO -- should it be added to old header, or popped off the end of self.headerArray?
            paddingSize = 0
            for i in range(4):
                paddingSize += (pow(256,(3-i)) * ord(self.headerArray[6+i]))

            self.oldHeaderLength += paddingSize

        #Okay, now we only have ID3v2 frames left. Lets start parsing them
        while len(self.headerArray) > 0:
            if self.headerArray[:4] == array('c','TIT2'):
                title = titleFrame()
                title.decode(self.popFrame())
                self.frames['TIT2'] = title
            elif self.headerArray[:4] == array('c','TPE1'):
                artist = artistFrame()
                artist.decode(self.popFrame())
                self.frames['TPE1'] = artist
            elif self.headerArray[:4] == array('c','TALB'):
                album = titleFrame()
                album.decode(self.popFrame())
                self.frames['TALB'] = album
            elif self.headerArray[:4] == array('c','TYER'):
                year = titleFrame()
                year.decode(self.popFrame())
                self.frames['TYER'] = year
            elif self.headerArray[:4] == array('c','TCON'):
                genre = titleFrame()
                genre.decode(self.popFrame())
                self.frames['TCON'] = genre
            elif self.headerArray[:4] == array('c','TRCK'):
                track = titleFrame()
                track.decode(self.popFrame())
                self.frames['TRCK'] = track
            elif self.headerArray[:4] == array('c','COMM'):
                comment = titleFrame()
                comment.decode(self.popFrame())
                frameID = comment.getFrameID()
                self.frames[frameID] = comment
            elif self.headerArray[:4].tostring() in ID3v2frames.id3TagsDict.otherTextInformationFrames.keys():
                frameID = self.headerArray[:4].tostring()
                otherframe = otherTextInformationFrame()
                otherframe.decode(self.popFrame())
                self.frames[frameID] = otherframe
            elif self.headerArray[:4] == array('c','\x00\x00\x00\x00'):
                #nullframe = blackBoxFrame()
                #nullframe.decode(self.popFrame())
                self.popFrame()
                #frameID = nullframe.getFrameID()
                # don't add it to self.frames, it's junk.
                #raise InvalidTagError('Frame with Null Tag. %s is probably corrupt' % (self.filename))
            else:
                blackbox = blackBoxFrame()
                blackbox.decode(self.popFrame())
                frameID = blackbox.getFrameID()
                self.frames[frameID] = blackbox

    def dump(self):
        """This is a debugging function that returns a list of dictionaries representing the frames in this
        ID3v2 tag."""
        dumpList= []
        for kw in self.frames.keys():
            dumpList.append(self.frames[kw].unpack())
        return dumpList

    def deltags(self):
        """Call this function to request that all tags be deleted. You must call write() in order to affect
        the deletion."""
        self.delete = 1
        self.modified = 1

    def write(self):
        """This function creates an MP3 with the proper tags embedded in it. It must be called before destroying
        an ID3v2 instance, or none of the changes will take effect."""
        if self.modified:
            #the spec says that tags appear 'in order significance
            # concering the recognition of the file'. I've decided this means:
            # TIT2,TRCK,TALB,TPE1,TYER,TCON,COMM
            header = array('B')
            for kw in self.frames.keys(): #TODO -- this should be a sorted list
                header.extend(self.frames[kw].encode())
                del self.frames[kw]

            #Figure out whether we need to unsynchronize. there should be a way to
            # turn this feature off.
            if header.count('\xFF') > 0:
                hlist = header.toList()
                for x in range(len(hlist)):
                    if hlist[x] == '\xFF' and (hlist[x+1] & '\xE0' == '\xE0'):
                        hlist.insert((x+1),'\x00')
                        self.unsynchronized = 1
                header.fromlist(hlist)

            #Calculate the flags before opening the file
            flags = '\x00'
            if self.unsynchronized:
                flags = flags & '\x80'
            if self.extendedHeader:
                flags = flags & '\x40'
            if self.experimentalTag:
                flags = flags & '\x20'
           

            try:
                #open a new file
                self.newfile = open(self.filename+'.tmp','w')

                #unless we've been asked to delete the tags, write tag info to new file
                if not self.delete:
                    self.newfile.write('ID3')

                    #Write Version number
                    self.newfile.write('\x03')
                    self.newfile.write('\x00')

                    self.newfile.write(flags)

                    hlength = len(header)
                    if hlength > pow(128,4):
                        raise InvalidTagError("Constructed tag too long; %s" % (self.filename))

                    for x in range(4):
                        if hlength >= pow(128,(3-x)):
                            self.newfile.write(chr((hlength - (hlength % pow(128,(3-x)))) / pow(128,(3-x))))
                            hlength = (hlength % pow(128,(3-x)))
                        elif hlength < pow(128,(3-x)):
		            self.newfile.write('\x00')

                    self.newfile.write(header.tostring())

                # Now copy the old MP3 data into the new tagged file
                self.oldfile = open(self.filename,'r')
                self.oldfile.seek(self.oldHeaderLength)

                self.newfile.write(self.oldfile.read())
                
                # close the files, flush the buffers
                self.oldfile.close()
                self.newfile.close()
                os.rename(self.filename+'.tmp',self.filename)
            except IOError, msg:
                pass

    def addFrame(self, frameDict):
        """This function takes a dictionary representing a frame, builds the frame object, and inserts it 
        into the tag. It uses a frames pack() method."""
        if frameDict['TAG'] == 'TIT2':
            title = titleFrame()
            title.pack(frameDict)
            if self.frames.has_key('TIT2') and title == self.frames['TIT2']:
                pass
            else:
                self.frames['TIT2'] = title
                self.modified = 1
        if frameDict['TAG'] == 'TPE1':
            artist = artistFrame()
            artist.pack(frameDict)
            if self.frames.has_key('TPE1') and artist == self.frames['TPE1']:
                pass
            else:
                self.frames['TPE1'] = artist
                self.modified = 1
        if frameDict['TAG'] == 'TALB':
            album = albumFrame()
            album.pack(frameDict)
            if self.frames.has_key('TALB') and album == self.frames['TALB']:
                pass
            else:
                self.frames['TALB'] = album
                self.modified = 1
        if frameDict['TAG'] == 'TYER':
            year = titleFrame()
            year.pack(frameDict)
            if self.frames.has_key('TYER') and year == self.frames['TYER']:
                pass
            else:
                self.frames['TYER'] = year
                self.modified = 1
        if frameDict['TAG'] == 'TCON':
            genre = genreFrame()
            genre.pack(frameDict)
            if self.frames.has_key('TCON') and genre == self.frames['TCON']:
                pass
            else:
                self.frames['TCON'] = genre
                self.modified = 1
        if frameDict['TAG'] == 'COMM':
            comment = commentFrame()
            comment.pack(frameDict)
            frameID = comment.getFrameID()
            if self.frames.has_key(frameID) and comment == self.frames[frameID]:
                pass
            else:
                self.frames[frameID] = comment
                self.modified = 1
        if frameDict['TAG'] == 'TRCK':
            track = trackFrame()
            track.pack(frameDict)
            if self.frames.has_key('TRCK') and track == self.frames['TRCK']:
                pass
            else:
                self.frames['TRCK'] = track
                self.modified = 1

    def delFrame(self, frameID):
        """Given the ID of a frame, this function will delete it. The frameID is usually, but not always, the 
        four word frame header listed in the ID3v2 specification."""
        del self.frames[frameID]
        self.modified = 1

    def popFrame(self):
        """This internal function pulls a frame from the the ID3v2 header. It is used in the initializer 
        to create the Frame objects."""
        size = 0
        if (len(self.headerArray) >= 14):
            for i in range(4):
              size += (pow(256,(3-i)) * ord(self.headerArray[4+i]))
            chunk = self.headerArray[:size+10]
            self.headerArray = self.headerArray[size+10:]
        else:
            chunk = self.headerArray
            self.headerArray = ''
        return chunk

    def sortFrames(self, x, y):
        """This doesn't work."""
        frameOrder = ['TIT2','TRCK','TALB','TPE1','TYER','TCON','COMM']
        try:
            frameOrder.index(x)
        except ValueError, msg:
            return 1

        try:
            frameOrder.index(x)
        except ValueError, msg:
            return -1

        return frameOrder.index(x) - frameOrder.index(y)
