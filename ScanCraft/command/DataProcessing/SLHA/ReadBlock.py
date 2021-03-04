#!/usr/bin/env python3

from functools import wraps
from .Accords import SLHA,MicrOMEGAs,matrixs
from ...operators.string import Dfloat
from .SLHA_line import LoopLines

additional_scalars={
    'SPhenoLowEnergy',
    'FlavorKitQFV',
    'INDIRECT_CHISQUARES'
}
additional_matrixs={
    'MUX','MV2','MX2','YV','TV','BMUX','LAMN','TLAMN', # 'SeeSaw
    'HiggsLHC13','HiggsLHC14','REDCOUP'
}

scalar_list=[ i.upper() for i in
    set( SLHA.keys() ) | set( MicrOMEGAs.keys() ) | additional_scalars
]
matrix_list=[ i.upper() for i in
    set( matrixs ) | additional_matrixs
]


@staticmethod
@LoopLines
def ReadScalar(line):
    s=line.split()
    code=int(s[0])
    value=Dfloat(s[1])
    return {code:value}
@staticmethod
@LoopLines
def ReadMatrix(line):
    s=line.split()
    code=(int(s[0]),int(s[1]))
    value=Dfloat(s[2])
    return {code:value}

from .special_blocks import special_blocks
class ReadBlock(special_blocks): # Container of methods to read SLHA data
    pass

for name in scalar_list:
    setattr(ReadBlock,name,ReadScalar)
for name in matrix_list:
    setattr(ReadBlock,name,ReadMatrix)