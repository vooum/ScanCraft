#! /usr/bin/env python3

import numpy
from ..color_print import Error
class scalar():
    def __init__(self,name,block,code,value=None):
        self.name   =   name
        self.block  =   block
        self.code   =   code
        self.value  =   value
    def __call__(self):
        return self.value

class matrix():
    def __init__(self,name,block,shape=None,value=None):
        self.name = name
        self.block= block
        # shape
        if isinstance(shape,(type(None),list,tuple)):
            self.shape=shape
        elif type(shape) is int:
            self.shape=(shape,shape)
        else:
            Error('wrong type of shape of matrix %s'(name))
        # value
        if type(value) in [type(None),numpy.ndarray]:
            self.value=value
        elif type(value) is list:
            self.value=numpy.asarray(value)
        elif type(value) is dict:
                row=max([i[0] for i in value.keys()])
                column=max([i[1] for i in value.keys()])
                self.value=numpy.zeros((row,column))
                for coords,v in value.items():
                    self.value[(coords[0]-1,coords[1]-1)]=v
        # set shape
        if (self.shape is None) and (self.value is not None):
            self.shape=self.value.shape

    def __call__(self,coords):
        return self.value((coords[0]-1,coords[1]-1))