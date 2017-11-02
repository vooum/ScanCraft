#! /usr/bin/env python3
import numpy
from .color_print import Error
class scalar:
    def __init__(self,name,block,PDG,value=None):
        self.name   =   name
        self.block  =   block
        self.PDG    =   PDG
        self.value  =   value
class matrix:
    def __init__(self,name,block,shape,element_list={}):
        self.name=name
        self.block=block
        self.shape=shape
        self.element_list=element_list

class data_list():
    pass


if __name__=='__main__':
    from color_print import ColorPrint
    # a=scalar('try','blockname',0,1.5)
    # print(type(a) is scalar)
    a=matrix('tryM','mx2',14.3)
    