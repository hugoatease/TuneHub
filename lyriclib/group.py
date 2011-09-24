#!/usr/bin/python
'''TuneHub Lyrics Library.
    Copyright (C) 2011  Hugo Caille
    
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer
    in the documentation and/or other materials provided with the distribution.
    3. The name of the author may not be used to endorse or promote products derived from this software without specific prior written permission.
    
    THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.'''

#This module fetch multiple lyrics at the same time from MetaHub. It's aim to speed-up lyrics download time.

import urllib2 #Used to grab files from HTTP.
import urllib #Contains tools for URL encoding.
#import zlib #Used to uncompress data returned by MetaHub.
import csv #Used to parse CSV data returned by MetaHub.

def stripcsv(str):
    lines = str.split('\n')
    inputlist = []
    for line in lines:
        line = line + '\n'
        inputlist.append(line)
    return inputlist

class Group:
    '''Class to fetch multiple lyrics on MetaHub. It takes as argument a list containing
    two-field dictionaries : Artist and Title.
    Example: [ {'Artist' : 'Sonic Youth', 'Title' : 'Teenage Riot'} , {'Artist' : 'Weezer', 'Title' : 'Hash Pipe'} ]
    The get() function will return data provided by MetaHub in dictionaries embeded in lists.'''
    
    def __init__(self, filter):
        self.filter = filter
        self.url = 'https://tunehubmeta.appspot.com/export'
    
    def makeCSV(self):
        vf = VirtualFile()
        csvapi = csv.writer(vf)
        csvapi.writerow(['Artist', 'Title'])
        
        for item in self.filter:
            try:
                csvapi.writerow( [ item['Artist'] , item['Title'] ] )
            except:
                pass
        
        self.csv = vf.get(compress=False)
        
    def exchange(self):
        parameters = {'csv' : self.csv}
        post = urllib.urlencode(parameters)
        data = urllib2.urlopen(self.url, post)
        data = data.read()
        self.fetched = data
        
    def parseCSV(self):
        csvapi = csv.reader(stripcsv(self.fetched))
        results = []
        for item in csvapi:
            try:
                data = {'Artist' : item[0], 'Title' : item[1], 'Lyric' : item[2], 'SiteID' : item[3], 'date' : item[4] }
                results.append(data)
            except:
                pass
        
        self.results = results
        return results
        
    def get(self):
        self.makeCSV()
        self.exchange()
        return self.parseCSV()
        
    
    
class VirtualFile:
    '''This class aims has a similar behaviour as file() object. It's used as an interface for csv module in writing operations.'''
    def __init__(self):
        self.csv = str()
        
    def write(self, str):
        self.csv = self.csv + str
            
    def get(self, compress=False):
        if compress:
            csvdata = zlib.compress(self.csv)
        else:
            csvdata = self.csv
        return csvdata

if __name__ == '__main__':
    request = []
    while 1:
        artist = raw_input('Artist: ')
        if len(artist) == 0:
            break
        title = raw_input('Title: ')
        
        dic = {'Artist' : artist, 'Title' : title}
        request.append(dic)
        
    print request
    api = Group(request)
    print api.get()