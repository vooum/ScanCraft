#!/usr/bin/env python3

from copy import deepcopy
from .SLHA_line import GetBlockName,GetDecayCode
from .ReadBlock import ReadBlock
from .ReadDecay import ReadDecay

class SLHA_text(object):
    '''need Python3.8 or higher version'''
    def __init__(self,text:list,block_format=ReadBlock):
        self.text=text
        self.current_line_number=0
        self.block_format=block_format
        self.menu={}# [case:(begin_line_number,end_line_number)]
        self.CheckMenu()
        self._BLOCK={}
        self._DECAY={}
    def CheckMenu(self):
        '''Split text into blocks and decays entil block/decay named of case.
        if case='all'(default), split all blocks'''
        last_case,start='head',0
        for i,line in enumerate(self.text):
            start=line[:5].upper()
            if 'BLOCK' == start:# block line
                current_case=GetBlockName(line) # str
            elif 'DECAY' == start:# decay line
                current_case=GetDecayCode(line) # int
            else:
                continue
            # find a case line
            end=i
            self.menu[last_case]=tuple(start,end)
            last_case,start=current_case,i
        # last line
        self.menu[current_case]=tuple(start,-1)
    def GetTextOfCase(self,case_name):
        try:
            start,end=self.menu[case_name]
        except KeyError:
            if type(case_name) is str:
                print(f'{block_name} not found in text')
            elif type(case_name) is int:
                print(f'DECAY for particle-{code} not found in text')
            raise
        return self.text[start:end]
    @property
    def block_dict(self):
        return {name:self.GetTextOfCase(name) for name in self.menu if type(name) is str}
    @property
    def decay_dict(self):
        return {name:self.GetTextOfCase(name) for name in self.menu if type(name) is int}
    def ReadBlock(self,block_name):
        text=self.GetTextOfCase(block_name)
        self._BLOCK[block_name]=getattr(self.block_format,block_name)(text)
        return self._BLOCK[block_name]
    def ReadDecay(self,code):
        text=self.GetTextOfCase(code)
        self._DECAY[code]=ReadDecay(text)
        return self._DECAY[code]
    def __call__(self,block:str,*code):
        if block in self.menu:
            data_dict=deepcopy(self._BLOCK[block])
            try:
                return data_dict[code[0]]
            except IndexError:
                return data_dict
            except KeyError:
                print(f'data with code:{code} not found in text:\n{self.GetTextOfCase[block]}')
                raise
        elif block=='DECAY':
            try:
                data_dict=deepcopy(self._DECAY[code[0]])
            except IndexError:
                print('please give the PDG-code of particle')
                raise
            try:
                return data_dict[code[1]]
            except IndexError:
                return data_dict
            except KeyError:
                print(f'data with code:{code} not found in text:\n{self.GetTextOfCase[code[0]]}')
                raise
        elif block=='WIDTH':
            try:
                data_dict=deepcopy(self._DECAY[code[0]])
            except IndexError:
                print('please give the PDG-code of particle')
                raise
            return data_dict['WIDTH']


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