#!/usr/bin/env python3

def Dfloat(string):
    try:
        return float(string)
    except ValueError:
        return float(string.upper().replace('D','E',1))

def StringToIFT(string:str):#translate string to int/float/tuple
    '''convert string to int/float/tuple if they are, and return it; else return string itself.
    '''
    try:# translate name
        trans=eval(string)
    except NameError:# can not translate string
        trans=string
    except SyntaxError:
        trans=string
    else:
        if type(trans) not in [int,float,tuple]:# unexcepted translate
            trans=string
    return trans