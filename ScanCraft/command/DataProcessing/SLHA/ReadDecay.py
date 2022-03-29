#!/usr/bin/env python3

import imp
from ...operators.string import Dfloat
from .LHA_line import LoopLines


# def FormatTo_float_tuple(line):
#     '''Get PDG tuple of final states'''
#     splited=line.split()
#     value=float(splited[0])
#     member_number=int(splited[1])
#     member_code=tuple([int(i) for i in splited[2:2+member_number]])
#     return {member_code: value}

@LoopLines
def ReadBranchRatio(line):
    '''Get PDG tuple of final states'''
    splited=line.split()
    value=float(splited[0]) # branch ratio
    member_number=int(splited[1]) # particle number of final states
    member_code=tuple([int(i) for i in splited[2:2+member_number]])
    return {member_code: value}


def ReadDecay(text):
    data={}
    splited=text[0].split()
    if splited[0].upper()=='DECAY':
        data['WIDTH'] = Dfloat(splited[2])
    branch_ratios = ReadBranchRatio(text)
    data.update(branch_ratios)
    return data

