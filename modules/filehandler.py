from os import listdir
import sys
sys.path.append('../lib/')

class Filer:
	def __init__(self, path):
		self.path = path
		
	def walkerCallback(self, filename):
		self.filelist.append(filename)
		
	def musiclist(self):
		from dirwalker import DirWalker
		walker = DirWalker()
		self.filelist = []
		walker.walk(self.path, self.walkerCallback)
		return self.filelist
		
	def mp3list(self):
		self.musiclist()
		files = self.filelist
		mp3list = []
		
		for file in files:
			test = file.split('.mp3')
			testlen = len(test)
			if testlen == 2:
				mp3list.append(file)
		self.mp3list = mp3list
		return mp3list
		
class OldFiler:

	def __init__(self, path):
		self.path = path

	def musiclist(__self__):
		path = __self__.path
		musicpath = path + 'iPod_Control/Music/'
		fnames = listdir(musicpath)
		listing = {}
		for item in fnames:
			item = musicpath + item + '/'
			listed = listdir(item)
			for item2 in listed:
				listlen = len(listing)
				name = item + item2
				listing[listlen] = name
		return listing


	def mp3list(__self__):
		listing = __self__.musiclist()
		mp3list = {}
		for item in listing:
			name = listing[item]
			test = name.split('.mp3')
			testlen = len(test)
			listlen = len(mp3list)
			if testlen == 2:
				mp3list[listlen] = name
		return mp3list
