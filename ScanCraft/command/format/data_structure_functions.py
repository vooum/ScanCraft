#!/usr/bin/env python3

FTL=lambda x: sum(map(FTL,x),[]) if isinstance(x,(list,tuple)) else [x]
def FlatToList(*Lists):
    '''
    extract all elements in multilayer lists and dict.keys()s to one list.
    '''
    # DL=[list(i)for i in Lists]
    return FTL([list(i)for i in Lists])