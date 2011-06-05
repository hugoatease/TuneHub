import urllib
import urllib2

class Sing365:
    
    def __init__(self, artist, title):
        self.keywords = artist + ' ' + title
    
    def search(self):
        keywords = self.keywords
        
        quoted = urllib.quote_plus(keywords)
        
        opener = urllib2.build_opener()
        headers = [('Referer', 'http://sing365.com/index.html'), ('Host', 'seek.sing365.com'), ('Accept-Language', 'en;q=1.0'), ('Accept-Encoding', 'gzip, compress, bzip, bzip2, deflate'), ('Accept', 'text/html, text/*;q=0.5, image/*'), ('User-Agent', 'w3m/0.5.3')]
        opener.addheaders = headers
        
        url = 'http://seek.sing365.com/cgi-bin/s.cgi?q=' + quoted + '&submit=go'
        request = opener.open(url)
        
        data = request.read()
        opener.close()
        
        toreturn = {'url': url, 'data': data}
        self.searchurl = url
        self.searchdata = data
        return toreturn
    
    def parseSearch(self):
        data = self.searchdata
        results=True
        result1 = None
        
        table = data.split('<table>')
        try:
            table = table[1]
            result1 = table.split('<td><b>1.</b></td>')
        except IndexError:
            results = False
            result1 = None
        
        
        try:
            if result1 != None:
                result1 = result1[1]
            else:
                results = False
        except IndexError:
            results = False
        
        if results == True:    
            link1 = result1.split('/music/lyric.nsf/')
            link1part1 = link1[0]
            link1part2 = link1[1]
            link1part1 = link1part1.split('<a href="')
            part1 = link1part1[1]
            
            link1part2 = link1part2.split('"')
            
            part2 = link1part2[0]
        
            url = part1 + '/music/lyric.nsf/' + part2
            
            self.lyricurl = url
            return url
        else:
            self.lyricurl = None
            return None
    
    def getLyricUrl(self):
        if self.lyricurl != None:
            lyricurl = self.lyricurl
            searchurl = self.searchurl
            
            opener = urllib2.build_opener()
            headers = [('Referer', searchurl), ('Host', 'www.sing365.com'), ('Accept-Language', 'en;q=1.0'), ('Accept-Encoding', 'gzip, compress, bzip, bzip2, deflate'), ('Accept', 'text/html, text/*;q=0.5, image/*'), ('User-Agent', 'w3m/0.5.3')]
            opener.addheaders = headers
            
            request = opener.open(lyricurl)
            data = request.read()
            request.close()
            
            self.lyricdata = data
            return data
        
        else:
            self.lyricdata = None
            return None

    
    def parseLyricPage(self):
        if self.lyricdata != None:
            data = self.lyricdata
            trim = data.split('<img src=http://www.sing365.com/images/phone2.gif border=0><br><br>')
            try:
                trim = trim[1]
                trim = trim.split('<br><img src=')
                html = trim[0]
                lines = html.split('<br>')
                lyrics = ''
                
                for line in lines:
                    lyrics = lyrics + line
                
                self.lyrics = lyrics
                return lyrics
            except:
                self.lyrics = None
                return None
        else:
            self.lyrics = None
            return None
        
    def filter(self):
        if self.lyrics != None:
            toreturn = False
            lyrics = self.lyrics
            count1 = lyrics.count('<')
            count2 = lyrics.count('>')
            
            if count1 > 5 and count2 > 5:
                self.lyrics = None
                toreturn = True
            
            if '(Instrumental)' in lyrics:
                self.lyrics = None
                toreturn = True
        
        
    
    def getLyric(self):
        keywords = self.keywords
        try:
            self.search()
            self.parseSearch()
            self.getLyricUrl()
            self.parseLyricPage()
            self.filter()
            lyrics = self.lyrics
        except:
            lyrics = 'Error'
        return lyrics
        