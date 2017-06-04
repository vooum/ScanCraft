#! /usr/bin/env python3
import numpy
from .color_print import Error
class scalar:
    def __init__(self,name,block,PDG,value):
        self.name   =   name
        self.block  =   block
        self.PDG    =   PDG
        self.value  =   value
class matrix:
    def __init__(self,name,block,shape,value):
        # if type(value) is numpy.ndarray or value==None:
        #     Error("value of '%s' should be type of numpy.ndarry"%name+
        #         "or leave None")
        #     exit()
        self.name=name
        self.block=block
        self.shape=shape
        self.value=value





if __name__=='__main__':
    from color_print import ColorPrint
    # a=scalar('try','blockname',0,1.5)
    # print(type(a) is scalar)
    a=matrix('tryM','mx2',14.3)
    