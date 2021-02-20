#!/usr/bin/env python3

from ...operators.string import Dfloat

def FormatTo_float_tuple(line):
    splited=line.split()
    value=float(splited[0])
    member_number=int(splited[1])
    member_code=tuple([int(i) for i in splited[2:2+member_number]])
    return {member_code: value}

def ReadDecay(text):
    data={}
    splited=text[0].split()
    if splited[0].upper()=='DECAY':
        data['WIDTH']=Dfloat(splited[2])
    for line in text:
        try:
            data.update(FormatTo_float_tuple(line))
        except ValueError: continue
        except IndexError: continue
    return data

