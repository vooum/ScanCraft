#!/usr/bin/env python3


FlatList=lambda x: sum(map(FlatList,x),[]) if isinstance(x,(list,tuple)) else [x]

def CapsuleToPandas(capsule_list):
    pass