#!/usr/bin/env python3

from collections import defaultdict
from .SLHA_line import GetBlockName


def int_code(line):
    c,_,*s=line.split(None,2)
    if s: end=s[0]
    else: end='\n'
    return int(c),end
def tuple_code(line):
    c1,c2,_,*s=line.split(None,3)
    if s: end=s[0]
    else: end='\n'
    return tuple((int(c1),int(c2))),end


class SetInputFile():
    def __init__(self,text_mold,point_mold,path):
        self.text_mold=text_mold
        self.path=path
        #Get all parameters
        data=defaultdict(dict)
        for par in point.variable_list:
            data[par.block][par.code]=par.value
            if type(par.code) is int:
                data[par.block]['code']=int_code
            elif type(par.code) is tuple:
                data[par.block]['code']=tuple_code
    def __call__(point):
        target=None
        for line in self.input_mold_lines:
            if line[0]=='#':pass
            else:
                start=line[:5].upper()
                if 'BLOCK' == start:
                    block=GetBlockName(line)
                    target=data.get(block)
                elif target:
                    code,end=target['code'](line)
                    value=target.get(code)