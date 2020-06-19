#!/usr/bin/env python3

from ...operators.object import lazyproperty
from .ReadBlock import ReadBlock
from .ReadDecay import ReadDecay
from collections import OrderedDict#,ChainMap

class SplitText(lazyproperty):
    '''
    Text will be seperated into partitions and store them in:
        instance.block_text & instance.decay_text
    Each partition start with a line start with 'BLOCK' or 'DECAY'.
    If any space or tab exist before 'BLOCK' or 'DECAY', that line will be ignored
    '''
    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            # This branch will be accessed by:
            # 'instance.SplitText_decorated_function()'
            instance.block_text=OrderedDict()
            instance.decay_text=OrderedDict()
            target=instance.block_text.setdefault('head',[])
            for line in instance.text:
                start=line[:5].upper()
                if 'BLOCK' == start:
                    target=instance.block_text.setdefault(GetBlockName(line),[])
                elif 'DECAY' == start:
                    target=instance.decay_text.setdefault(GetDecayCode(line),[])
                target.append(line)
            return getattr(instance,self.func.__name__)


class SLHA_block:
    '''block'''
    def __init__(self,block_text,block_format=ReadBlock):
        self.text_dict=block_text
        self.block_format=block_format
    def __getattr__(self,block_name):
        # print(f'find {block_name}')
        try: text=self.text_dict[block_name]
        except KeyError: 
            print(f'{block_name} not found in text')
            raise
        try: data=getattr(self.block_format,block_name)(text)
        except AttributeError:
            print(f'Load method for {block_name} not found in block_format')
            print(*self.text_dict[block_name])
            raise
        setattr(self,block_name,data)
        return data

class SLHA_decay:
    '''particals' decay information'''
    def __init__(self,decay_text):
        self.text_dict=decay_text
        self.data={}

    def ReadDecay(self,p_code=None):
        if p_code is None:
            for p_code in self.text_dict.keys():
                self.ReadDecay(p_code)
        else:
            try: text=self.text_dict[p_code]
            except KeyError:
                print(f'DECAY for particle-{code} not found in text')
                raise
            self.data[p_code]=ReadDecay(text)
    def __getitem__(self,p_code):
        try: return self.data[p_code]
        except KeyError:
            self.ReadDecay(p_code)
            return self[p_code]
    def __getattr__(self,p_str):
        if p_str[0]=='p':
            return self[int(p_str[1:])]
        else:
            print(f'Wrong Key: {p_str}')
            print(r'argument "p_str" should be p{PDG} like p24 for Z decay')

class SLHA_text(object):
    '''extracted messages from SLHA text'''
    def __init__(self,text,block_format=ReadBlock):
        self.text=text
        self.block_format=block_format
    @SplitText
    def block_text(self): pass
    @SplitText
    def decay_text(self): pass
    @lazyproperty
    def DECAY(self):
        return SLHA_decay(self.decay_text)
    @lazyproperty
    def BLOCK(self):
        return SLHA_block(self.block_text,block_format=self.block_format)
    def __call__(self,name,*code):
        name=name.upper()
        if name in self.block_text.keys():
            data_dict=getattr(self.BLOCK,name)
            try:
                return data_dict[code[0]]
            except KeyError:
                print(f'data with code:{code} not found in text:\n{data_dict}')
                raise
            except IndexError:
                if len(code)==0:
                    return getattr(self.BLOCK,name)
                else: # just in case
                    raise
        elif name=='DECAY':
            data_dict=self.DECAY[code[0]]
            try:
                return data_dict[code[1]]
            except KeyError:
                print(f'data with code:{code} not found in text:\n{data_dict}')
                raise
        elif name=='WIDTH':
            return self.DECAY[code[0]]['WIDTH']

class SLHA_document(SLHA_text):
    '''extracted messages from SLHA file'''
    def __init__(self,SLHA_document,block_format=ReadBlock):
        self.path=SLHA_document
        self.block_format=ReadBlock
    @lazyproperty
    def text(self):
        # print(f'Getting text from {self.path}')
        with open(self.path,'r') as SLHA:
            return SLHA.readlines()