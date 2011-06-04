from urllib import quote
import urllib2

class MLDB:
    
    def __init__(self, artist, title):
            self.artist = artist
            self.title = title
            
    def search(self):
            keywords = self.artist + ' ' + self.title
            keywords = quote(keywords)
            url = 'http://www.mldb.org/search?mq=' + keywords + '&si=0&mm=0&ob=1'
            urlobj = urllib2.urlopen(url)
            data = urlobj.read()
            urlobj.close()
            current = urlobj.geturl()
            if 'http://www.mldb.org/song-' in current:
                    self.songsrc = data
                    return 'song'
            else:
                    self.searchsrc = data
                    return 'search'

    def songParse(self):
            data = self.songsrc
            data = data.split('<p class="songtext" lang="EN">')
            lyrics = data[1]
            lyrics = lyrics.split('</p>')
            lyrics = lyrics[0]
            lines = lyrics.split('<br />')
            lyrics = ''
            for line in lines:
                    lyrics = lyrics + line
            return lyrics

    def searchParse(self):
            data = self.searchsrc
            try:
                    data = data.split('<a href="song-')
                    data = data[1]
                    data = data.split('">')
                    data = data[0]
            except IndexError:
                    data = 0

            if data !=0:
                    url = 'http://www.mldb.org/song-' + data
            
                    urlobj = urllib2.urlopen(url)
                    self.songsrc = urlobj.read()
                    urlobj.close()
            else:
                    self.songsrc = 0

    def getLyric(self):
            searchpage = self.search()

            if searchpage == 'song':
                    lyrics = self.songParse()
                    return lyrics
            elif searchpage == 'search':
                    lyricsurl = self.searchParse()
                    if self.songsrc != 0:
                            lyrics = self.songParse()
                            return lyrics			
                    else:
                            return None
            else:
                    return None
