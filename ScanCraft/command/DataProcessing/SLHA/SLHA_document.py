#!/usr/bin/env python3

from collections import OrderedDict#,ChainMap
from .ReadLine import GetBlockName,GetDecayCode
from ...operators.iterable import FlatToList
from ...operators.object import lazyprogerty

class SLHA_line:
    '''line in SLHA format'''
    

class SLHA_block:
    '''block'''
    def __init__(self,block_name):
        pass
class SLHA_decay:
    '''particals' decay information'''
    def __init__(self,decay_text):
        print(decay_text.keys())

def SplitText_triger(func):
    print(func.__name__)
    @property
    def Split(self):
        print('split')
        self.SplitText()
        return self
    return Split


class SLHA_text:
    '''extracted messages from SLHA file'''
    def __init__(self,text):
        self.text=text
    def SplitText(self):
        print('text')
        self.block_text=OrderedDict()
        self.decay_text=OrderedDict()
        # self.data=ChainMap(self.blocks,self.decays)
        # block_name='head' # to store messages before first block
        target=self.block_text.setdefault('head',[])
        for line in self.text:
            start=line[:5].upper()
            if 'BLOCK' in start:
                target=self.block_text.setdefault(GetBlockName(line),[line])
            elif 'DECAY' in start:
                target=self.decay_text.setdefault(GetDecayCode(line),[line])
            else:
                target.append(line)
    @SplitText_triger
    def block_text(self):
        pass
    @lazyprogerty
    def decay_text(self):
        self.SplitText()
        return self.decay_text
    @lazyprogerty
    def DECAY(self):
        return SLHA_decay(self.decay_text)
    @lazyprogerty
    def BLOCK(self):
        return SLHA_block(self.block_text)
    def __getattr__(self,block,*code_list):
        try:
            return self.BLOCK[block]
        except KeyError:
            raise
        code=iter(code_list)

class SLHA_document(SLHA_text):
    def __init__(self,SLHA_document):
        with open(SLHA_document,'r') as SLHA:
            super().__init__(SLHA.readlines())
        self.path=SLHA_document