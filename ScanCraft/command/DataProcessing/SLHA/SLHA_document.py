#!/usr/bin/env python3

from collections import OrderedDict
from .ReadLine import GetBlockName,GetDecayCode

class SLHA_line:
    '''line in SLHA format'''
    

class SLHA_block:
    '''block'''
    def __init__(self,block_name):
        pass
class SLHA_decay:
    '''particals' decay information'''
    def __init__(self,particle_code):
        pass

class SLHA_text:
    '''extracted messages from SLHA file'''
    def __init__(self,text):
        self.text=text
        self.blocks=OrderedDict()
        self.decays=OrderedDict()
        block_name='head' # to store messages before first block
        target=self.blocks.setdefault('head',[])
        for line in self.text:
            start=line[:5].upper()
            if 'BLOCK' in start:
                target=self.blocks.setdefault(GetBlockName(line),[])
            elif 'DECAY' in start:
                target=self.decays.setdefault(GetDecayCode(line),[])
            else:
                target.append(line)

def SLHA_document(SLHA_document):
    with open(SLHA_document,'r') as SLHA:
        return SLHA_text(SLHA.readlines())