#!/usr/bin/env python3

from ...operators.object import lazyprogerty



class SLHA_block:
    '''block'''
    def __init__(self,block_text):
        self.text_dict=block_text
    def __getattr__(self,name)

    # def __setattr__(self):
    #     pass
    # def __getattr__(self):
    #     pass