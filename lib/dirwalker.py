#Class originally published on http://ssscripting.wordpress.com/2009/03/03/python-recursive-directory-walker/
import os,sys

class DirWalker(object):

    def walk(self,dir,meth):
    #walks a directory, and executes a callback on each file
                dir = os.path.abspath(dir)
                for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
                        nfile = os.path.join(dir,file)
                        meth(nfile)
                        if os.path.isdir(nfile):
                                try:
                                        self.walk(nfile,meth)
                                except OSError:
                                        pass
            