#! /usr/bin/env python3
import os
def _GetSphenoDir():
    position=os.path.dirname(os.path.dirname(__file__))
    for i in os.listdir(os.path.join(position,'packages/')):
        #print(i)
        if 'SPheno' in i and os.path.isdir(i):
class Spheno():
    def __init__(self,Dir=_GetSphenoDir()):
        pass