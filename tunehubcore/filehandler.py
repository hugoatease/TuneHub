'''TuneHub Core Library.
    Copyright (C) 2011  Hugo Caille

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

from os import listdir

class Filer:
	def __init__(self, path):
		self.path = path
		
	def walkerCallback(self, filename):
		self.filelist.append(filename)
		
	def musiclist(self):
		from tunehubcore import dirwalker
		walker = dirwalker.DirWalker()
		self.filelist = []
		walker.walk(self.path, self.walkerCallback)
		return self.filelist
		
	def supportedList(self):
		self.musiclist()
		files = self.filelist
		list = []
		
		for file in files:
			ismp3 = '.mp3' in file
			ism4a = '.m4a' in file
			isvorbis = '.ogg' in file
			if ismp3 or ism4a or isvorbis:
				list.append(file)
		self.list = list
		return list
		
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
