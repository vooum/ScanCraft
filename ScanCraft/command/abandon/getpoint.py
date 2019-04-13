#!/usr/bin/env python3
from ..read.readSLHA import * 
def GetPoint(point,inp):
    S=readSLHA()
    S.read(inp)
    ParameterList=point.VariableList
    BLOCK=''
    for name in ParameterList:
        Pari=getattr(point,name)
        Pari.value=getattr(S,Pari.block)[Pari.PDG]
    return
    