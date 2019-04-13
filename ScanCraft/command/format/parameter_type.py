#! /usr/bin/env python3

import numpy
# from collections import namedtuple
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
        if value is None:
            self.value=None
        else:
            self.Set_value(value)
        # shape
        if isinstance(shape,(type(None),list,tuple)):
            self.shape=shape
        elif type(shape) is int:
            self.shape=(shape,shape)
        else:
            Error('wrong type of shape of matrix %s'(name))

    def Set_value(new_value):
        # set value
        if type(new_value) is numpy.ndarray:
            self.value=value
        elif type(new_value) is list:
            self.value=numpy.asarray(new_value)
        elif type(new_value) is dict:
                row=max([i[0] for i in new_value.keys()])
                column=max([i[1] for i in new_value.keys()])
                self.value=numpy.zeros((row,column))
                for coords,v in new_value.items():
                    self.value[(coords[0]-1,coords[1]-1)]=v
        # set shape
        if self.shape is None:
            self.shape=self.value.shape
    def __call__(self,coords):
        return self.value((coords[0]-1,coords[1]-1))

class data_list():
    pass