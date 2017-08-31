#!/usr/bin/env python3
import copy
def KeyOfMaxValue(Dict):
    mk,mv='',0.
    for k,v in Dict.items():
        if v>mv:
            mk=k
            mv=v
        #print(k,v,mk,mv)
    return mk
def KeyOfMinValue(Dict):
    mk,mv='',1.e99
    for k,v in Dict.items():
        if v<mv:
            mk=k
            mv=v
        #print(k,v,mk,mv)
    return mk

def MaxN1Conponent(sample):
    Component={
                'B':sample.Nmix[(1,1)]**2
               ,'W':sample.Nmix[(1,2)]**2
               ,'H':sample.Nmix[(1,3)]**2+sample.Nmix[(1,4)]**2
               ,'S':sample.Nmix[(1,5)]**2
              }
    k=KeyOfMaxValue(Component)
    #print(k,Component)
    return k

def GetLSP(sample):
    SpList=copy.deepcopy(list(sample.MASS.keys()))
    SpDict={}
    for i in SpList:
        if int(i) > 1e6:
            SpDict[i]=abs(sample.MASS.get(i))
    SpDict.pop(1000039)
    return KeyOfMinValue(SpDict)