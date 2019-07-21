#!/usr/bin/env python3

class SLHA_line:
    '''line in SLHA format'''
    

class SLHA_block:
    '''block'''
    def __init__(self,block_name):

class SLHA_decay:
    '''particals' decay information'''
    def __init__(self,particle_code):

class SLHA_document:
    '''extracted messages from SLHA file'''
    def __init__(self,SLHA_file):
        with open(SLHA_file,'r') as SLHA:
            self.text=SLHA.readlines()
        self.blocks={}
        block_name='head' # to store messages before first block
        for line in self.text:
            if　'BLOCK' in line[:5].upper():
                block_name=line[5:]
            elif 'DECAY' in start:
                pass