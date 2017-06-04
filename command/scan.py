#!/usr/bin/env python3
import numpy
from .data_type import scalar,matrix
from .read.readline import ReadLine
from .color_print import *

class scan():
    def __init__(self,method='mcmc'):
        self.variable_list={}
        self.scalar_list={}
        self.matrix_list={}
        self.block_list={}
        self.Add=self.AddMcmcScalar
        self.AddMatrix=self.AddMcmcMatrix

    def AddMcmcScalar(self,name,block,PDG,minimum=None,maximum=None,pace='normal',step_width=None,value=None):
        block=block.upper()

        # set one scalar
        scl=scalar(name,block,PDG,value)
        
        # set scan strategy
        pace=pace.lower().split()
        if pace[0] not in ('normal','lognormal','follow'):
            Caution("'pace' should be 'normal', 'lognormal' or 'follow name_of_target'")
            exit()
        scl.pace=pace[0]
        if scl.pace!='follow':
            scl.minimum=minimum
            scl.maximum=maximum
        else:
            scl.target=pace[1]
        if step_width:
            scl.step_width=step_width
        else:
            try:
                scl.step_width=(scl.maximum-scl.minimum)/1000.
            except TypeError:
                Caution(
                    "  Both maximum and minimum of '%s' should be given with pace='%s'"%(name,pace[0])
                +   " if step width is not specified. Later, step width will be 1% of its initial value")
                pass

        # add scalar into lists
        if name in self.variable_list.keys():
            Caution("scalar '%s' overridden"%name)
        self.variable_list[name]=scl

        if block not in self.block_list.keys():
            self.block_list[block]={}
        block_i=self.block_list[block]
        block_i[PDG]=scl
    
    def AddMcmcMatrix(self,name,block,shape,free_element=[],minimum=None,maximum=None,pace='normal',step_width=None,value=None):
        block=block.upper()
        # set one matrix
        mtx=matrix(name,block,shape,value)
        mtx.free_element=[]
        if type(free_element) is str:
            pass
        else:
            if (type(free_element[0]) is tuple) or (type(free_element[0]) is list):
                for i in free_element:
                    mtx.free_element.append(tuple(i))
        mtx.element_list=dict.fromkeys(mtx.free_element)

        mtx.minimum=minimum
        mtx.maximum=maximum
        mtx.pace=pace
        mtx.step_width=step_width

        # add matrix into lists
        if name in self.variable_list.keys():
            Caution("parameter '%s' overridden"%name)
        self.variable_list[name]=mtx

        if block in self.block_list.keys():
            Caution("matrix '%s' overridden"%name)
        self.block_list[block]=mtx