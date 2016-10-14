#!/usr/bin/env python3
from .readSLHA import * 
def GetPoint(point,inp):
    S=readSLHA()
    S.read(inp)
    ParameterList=point.list
    BLOCK=''
    for name in ParameterList:
        Pari=getattr(point,name)
        #print(S.EXTPAR)
        #print(S.MINPAR,Pari.block)
        Pari.value=getattr(S,Pari.block)[Pari.PDG]
        print(name,Pari.value)
    return