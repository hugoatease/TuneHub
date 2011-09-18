#!/usr/bin/env python

from distutils.core import setup

setup(name='TuneHub', version='0.2', description='A tool for fetching lyrics on Internet and manage them', author='Hugo Caille', author_email='hugo@gkz.fr.nf', url='http://www.tunehub.tk', license='GNU GPL v.3', packages=['lyriclib','tunehubcore', 'progressbar', 'xmltodict'], package_dir={'progressbar': 'lib/', 'xmltodict': 'lib/'}, scripts=['tunehub.py'])
