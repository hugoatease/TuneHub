# -*- coding: utf-8 -*-

try:
    import gpod #Import de la librairie GtkPod. Si elle n'est pas disponible, création d'une variable pour l'utilisation en ligne.
    mode = 'local'
except ImportError:
    mode = 'remote'
    
class iPod:
    #Cette classe permet d'indiquer à l'iPod qu'il existe des paroles dans le tag ID3.
    #Si libgpod n'est pas installée (Windows), utilise un service en ligne.
    
    def __init__(self, mount):
        self.mount = mount #Mountpoint de l'iPod
        #Passe le mode de traitement à la classe
        global mode
        self.mode = mode
        self.list = [] #Liste de fichiers à modifier
        self.total = 0
        self.done = 0
        
    def flag(self, artist, title):
        #Ajoute un fichier à la liste des fichiers à modifier.
        toadd = {'Artist' : artist, 'Title' : title}
        self.list.append(toadd)
        self.total = self.total + 1
        
    def success(self):
        self.done = self.done + 1

    def make(self):
        if self.mode == 'local':
            self.makeLocal()
        if self.mode == 'remote':
            self.makeRemote()
    
    def makeRemote(self):
        print 'Remote iPod flagging is not supported yet.'
            
    def makeLocal(self):
        self.itdb = gpod.itdb_parse(self.mount, None)
        for track in gpod.sw_get_tracks(self.itdb):
            title = track.title
            artist = track.artist
            if {'Artist' : artist, 'Title' : title} in self.list:
                track.lyrics_flag = 1
                
            gpod.itdb_write_file(self.itdb, 'iTunesDB', None)
