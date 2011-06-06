#!/usr/bin/python
import sys
sys.path.append("modules/")

import pickle

f = open('lyrics.db')
data = pickle.load(f)
f.close()

from txtexporter import TxtExport

for item in data:
    motor = TxtExport(item)
    motor.make()