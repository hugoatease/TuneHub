import sys
sys.path.append("modules/")

import pickle

f = open('lyrics.db')
data = pickle.load(f)
f.close()

from txtexport import TxtExport

for item in data:
    motor = TxtExport(item)
    motor.make()