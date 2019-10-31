#! /usr/bin/env python3

import copy
from collections import defaultdict
from ..DataProcessing.SLHA.SLHA_line import GetBlockName


def int_code(line):
    c,_,*s=line.split(None,2)
    return int(c),s
def tuple_code(line):
    c1,c2,_,*s=line.split(None,3)
    return tuple((int(c1),int(c2))),s

class GenerateLine():
    '''
    This class is used to generate each line which should be motified
    in creating an input file. One line for one parameter.
    __init__:
        input parameters for initialization:
            block:str: block name
            code:int/tuple: code for the parameter.
            end:list: list of annotation strings to be appended after value and a '#'
    __call__:
        input:dict: point
            format: {block_name:{code:value,},}
            value:float
        return:Line with parameter value subsituted, like:
            '\t3\t2\t# annotations'
    '''
    def __init__(self,block:str,code,end:list):
        self.block=block
        self.code=code
        if type(code) is int:
            self.code_str=str(code)
        elif type(code) is tuple:
            self.code_str=' '.join(str(i) for i in code)
        self.end=''.join(['\t'+i.rstrip('\n') for i in end])
    def __call__(self,point_dict):
        value=point_dict[self.block][self.code]
        return f'\t{self.code_str}\t{value}{self.end}'

class unchanged_line():
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
        target_block=None
        for i,line in enumerate(text_mold):
            if line[0]=='#':pass # annotation
            else:
                start=line[:5].upper()
                if 'BLOCK' == start:
                    block=GetBlockName(line)
                    target_block=point_dict.get(block)
                elif target_block: # lines to change in this block
                    try:
                        code,end=target_block['code'](line)
                    except ValueError: # maybe ampty line
                        pass
                    else:
                        if code in target_block: # find parameter in point_mold
                            generator=GenerateLine(block,code,end)
                            generators.append(generator)
                            continue
            generators.append( unchanged_line(line) )
        self.generators=generators
    def __call__(self,point_dict):
        lines=[f(point_dict)+'\n' for f in self.generators]
        lines[-1].rstrip('\n')
        with open(self.path,'w') as inp:
            inp.writelines(lines)

def GetSLHAValues(point):
    point_dict=defaultdict(dict)
    for par in point.variable_dict.values():
        point_dict[par.block][par.code]=par.value
    return point_dict

class GenerateInputWithScan(GenerateInputFile):
    def __init__(self, text_mold, point, path):
        point_dict=GetSLHAValues(point)
        super().__init__(text_mold, point_dict, path)
    def __call__(self, point):
        point_dict=GetSLHAValues(point)
        super().__call__(point_dict)