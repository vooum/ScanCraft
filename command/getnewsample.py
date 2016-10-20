#!/usr/bin/env python3
from .mcmc import *
import random
class Sample():
    pass

def GetNewSampleFrom(Old):
    New=sample()
    for name in Old.list:
        O=getattr(Old,name)
        new_value=random.uniform(O.min,O.max)
        setattr(New,name,Parameter(O.name,O.block,O.PDG,new_value))
        if not hasattr(New,O.block):
            setattr(New,O.block,{})
        getattr(New,O.block)[O.PDG]=getattr(New,name)
        getattr(New,O.block)[O.name]=getattr(New,name)
    return New