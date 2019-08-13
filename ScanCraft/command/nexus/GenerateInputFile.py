#! /usr/bin/env python3

import copy
from collections import defaultdict
from ..DataProcessing.SLHA_line import GetBlockName

def GetSLHAValues(point):
    point_dict=defaultdict(dict)
    for par in point.variable_dict.values():
        point_dict[par.block][par.code]=par.value
    return point_dict

def int_code(line):
    c,_,*s=line.split(None,2)
    return int(c),s
def tuple_code(line):
    c1,c2,_,*s=line.split(None,3)
    return tuple((int(c1),int(c2))),s

class GenerateLine():
    def __init__(self,block:str,code,end:list):
        self.block=block
        self.code=code
        if type(code) is int:
            sequence=[str(code)]
            self.value_index=1
        elif type(code) is tuple:
            sequence=[str(i) for i in code]
            self.value_index=2
        annotation=[i.rstrip('\n') for i in end]
        sequence.extend(annotation)
        self.sequence=sequence
    def __call__(self,point):
        value_str=str(point.block_list[self.block][self.code].value)
        self.sequence.insert(self.value_index,value_str)
        return '\t'+'\t'.join(self.sequence)

class unchange_line():
    def __init__(self,line):
        self.line=line.rstrip('\n')
    def __call__(self,point):
        return self.line

class GenerateInputFile():
    def __init__(self,text_mold,point_dict,path):
        self.text_mold=text_mold
        self.path=path
        #Get all parameters
        for block in point_dict.values():
            code_type=type(list(block.keys())[0])
            if code_type is int:
                block['code']=int_code
            elif code_type is tuple:
                block['code']=tuple_code
        # set input_file generators
        generators=[]
        target=None
        for i,line in enumerate(text_mold):
            if line[0]=='#':pass # annotation
            else:
                start=line[:5].upper()
                if 'BLOCK' == start:
                    block=GetBlockName(line)
                    target=point_dict.get(block)
                elif target: # lines to change in this block
                    try:
                        code,end=target['code'](line)
                    except ValueError: # maybe ampty line
                        pass
                    else:
                        if code in target: # find parameter in point_mold
                            generator=GenerateLine(block,code,end)
                            generators.append(generator)
                            continue
            generators.append( unchange_line(line) )
        self.generators=generators
    def __call__(self,point):
        lines=[f(point)+'\n' for f in self.generators]
        lines[-1].rstrip('\n')
        with open(self.path,'w') as inp:
            inp.writelines(lines)