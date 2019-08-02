#!/usr/bin/env python3

# from ...operators.object import lazyprogerty
from .SLHA_line import ReadLine,commented_out
from functools import wraps

scalar_groups={
    'SUSY_input':   ['MINPAR','EXTPAR'],
    'additional':   ['NMSSMRUN','MSOFT'],
    'output'    :   ['MASS','SPhenoLowEnergy','FlavorKitQFV','LOWEN','LHCFIT','FINETUNING'],
    'omega'     :   ['ABUNDANCE','LSP','NDMCROSSSECT','INDIRECT_CHISQUARES']
}
matrix_groups={
    'Mass'      :   ['MSD2','MSE2','MSL2','MSQ2','MSU2'],
    'Mix'       :   ['NMHMIX','NMAMIX','STOPMIX','NMNMIX'],
    'Triliner'  :   ['TD','TE','TU'],
    'SeeSaw'    :   ['MUX','MV2','MX2','YV','TV','BMUX','LAMN','TLAMN'],
    'output'    :   ['YE','YU','YD',
                     'HiggsLHC13','HiggsLHC14','REDCOUP']
}
scalar_list=[ i.upper() for j in scalar_groups.values()  for i in j ]
matrix_list=[ i.upper() for j in matrix_groups.values()  for i in j ]

def LoopLines(func):
    '''
    Read SLHA informations line by line with wrapped functions.
    Return a dictionary
    '''
    @wraps(func)
    def wrapper(lines,*args,**kwargs):
        data=dict()
        for line in lines:
                data.update(func(line))
        return data
    return wrapper

def Dfloat(string):
    try:
        return float(string)
    except ValueError:
        return float(string.upper().replace('D','E',1))

@LoopLines
def ReadScalar(line):
    s=line.split()
    try:
        code=int(s[0])
        value=Dfloat(s[1])
    except ValueError: return {}
    except IndexError: return {}
    else: return {code:value}

@LoopLines
def ReadMatrix(line):
    s=line.split()
    try:
        code=(int(s[0]),int(s[1]))
        value=Dfloat(s[2])
    except ValueError: return {}
    except IndexError: return {}
    else: return {code:value}

class ReadBlock(): # Container of methods to read SLHA data
    pass

for name in scalar_list:
    setattr(ReadBlock,name,ReadScalar)
for name in matrix_list:
    setattr(ReadBlock,name,ReadMatrix)

class SLHA_block:
    '''block'''
    def __init__(self,block_text,block_format=ReadBlock):
        self.text_dict=block_text
        self.block_format=block_format
    def __getattr__(self,block_name):
        # print(f'find {block_name}')
        text=self.text_dict[block_name]
        data=getattr(self.block_format,block_name)(text)
        setattr(self,block_name,data)
        return data
    def __setattr__(self,block_name,data):
        pass