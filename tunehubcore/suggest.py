#!/usr/bin/python
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
    
#This module provides a class which aims to give a list of title suggestions based on one song title.
#It helps to correct wrong music titles

from musicbrainz2 import webservice as ws
import difflib

q=ws.Query()

class Suggest:
    def __init__(self, artist, album, title):
        self.artist = artist
        self.title = title
        self.album = album
        
    def TrackList(self, artist=None, album=None, limit=100):
        if artist == None or album == None:
            artist = self.artist
            album = self.album
        filter = ws.TrackFilter(artistName = artist, releaseTitle= album)
        results = q.getTracks(filter)
        listing = []
        for result in results:
            listing.append(result.track.title)
        self.listing = listing
        return listing
    
    def top(self, title=None, listing=None):
        if listing == None or title == None:
            title = self.title
            listing = self.listing
        top = {}
        for item in listing:
            s = difflib.SequenceMatcher(None, title.lower(), item.lower())
            ratio = s.ratio()
            if ratio > 0.4:
                top[item] = ratio
        
        sort = sorted(top, key=lambda x : top[x], reverse=True) #Trie les titres en ordre de valeur croissante
        self.top = sort
        return sort
        
    def get(self):
        self.TrackList()
        top = self.top()
        return top
        
    
if __name__ == '__main__':
    artist = raw_input('Artist: ')
    album = raw_input("Album: ")
    title = raw_input('Title: ')
    sug = Suggest(artist, album, title)
    print sug.get()