#!/usr/bin/env python

import os
scriptname = 'tunehub.py'
if os.path.isfile('tunehub') == False:
    try:
        f = open('tunehub.py', 'r')
        code = f.read()
        f.close()
        f = open('tunehub', 'w')
        f.write(code)
        f.close()
        scriptname = 'tunehub'
    except:
        pass
else:
	scriptname = 'tunehub'        
    

from distutils.core import setup

setup(name='TuneHub', version='0.2', description='A tool for fetching lyrics on Internet and manage them', author='Hugo Caille', author_email='hugo@gkz.fr.nf', url='http://www.tunehub.tk', license='GNU GPL v.3', packages=['lyriclib','tunehubcore'], py_modules=['progressbar'], scripts=[scriptname])

