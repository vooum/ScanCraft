#!/usr/bin/env python3

from collections import OrderedDict#,ChainMap
from .ReadLine import GetBlockName,GetDecayCode
from ...operators.iterable import FlatToList
from ...operators.object import lazyprogerty
from .SLHA_block import SLHA_block

class SLHA_line:
    '''line in SLHA format'''
    

class SLHA_decay:
    '''particals' decay information'''
    def __init__(self,decay_text):
        self.text_dict=decay_text
    

class SplitText(lazyprogerty):
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            # instance.SplitText()
            instance.block_text=OrderedDict()
            instance.decay_text=OrderedDict()
            target=instance.block_text.setdefault('head',[])
            for line in instance.text:
                start=line[:5].upper()
                if 'BLOCK' in start:
                    target=instance.block_text.setdefault(GetBlockName(line),[line])
                elif 'DECAY' in start:
                    target=instance.decay_text.setdefault(GetDecayCode(line),[line])
                else:
                    target.append(line)
            return getattr(instance,self.func.__name__)

class SLHA_text:
    '''extracted messages from SLHA file'''
    def __init__(self,text):
        self.text=text
    @SplitText
    def block_text(self): pass
    @SplitText
    def decay_text(self): pass
    @lazyprogerty
    def DECAY(self):
        return SLHA_decay(self.decay_text)
    @lazyprogerty
    def BLOCK(self):
        return SLHA_block(self.block_text)
    def __getattr__(self,block,*code_list):
        try:
            print('get')
            return self.BLOCK
        except KeyError:
            raise
        code=iter(code_list)

class SLHA_document(SLHA_text):
    def __init__(self,SLHA_document):
        self.path=SLHA_document
    @lazyprogerty
    def text(self):
        # print(f'Getting text from {self.path}')
        with open(self.path,'r') as SLHA:
            return SLHA.readlines()
