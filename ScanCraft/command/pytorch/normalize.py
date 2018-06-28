#!/usr/bin/env python3

import numpy
from ..data_transformer.defult_parameter_order import defult_name_order
from ..data_transformer.InputToPandas import InputToPandas
def GetRanges(par_dict,order=None):
    '''generate an array contains minimums and maximums of the input parameter dictionary with given order'''
    if order is None:
        order=defult_name_order(par_dict)
    ranges=numpy.array(
        [
            [par_dict[i].minimum for i in order],
            [par_dict[i].maximum for i in order]
        ]
    )
    return ranges

def NormalizeArray(array,par_ranges,scale=(0,1)):
    return (array-par_ranges[0])*(scale[1]-scale[0])/(par_ranges[1]-par_ranges[0])+scale[0]
def DenormalizeArray(array,par_ranges,scale=(0,1)):
    return (array-scale[0])*(par_ranges[1]-par_ranges[0])/(scale[1]-scale[0])+par_ranges[0]

def NormalizePointListToPandas(point_list,order=None,title=None):
    if order is None:
        order=defult_name_order(point_list[0].free_parameter_list)
    if title is None:
        title='normalized'
    par_ranges=GetRanges(point_list[0].free_parameter_list,order=order)
    raw=InputToPandas(point_list,order=order,title=title)
    normalized=NormalizeArray(raw,par_ranges)
    return normalized

def DenormalizeUniform(array,mold,order=None):
    if order is None:
        order=defult_name_order(mold.free_parameter_list)
    par_ranges=GetRanges(mold.free_parameter_list,order=order)
    array=(array/2.+1.)*(par_ranges[1]-par_ranges[0])+par_ranges[0]
    return array

class normalize():
    def __init__(self,mold,order=None,scale=None):
        if order is None:
            order=defult_name_order(mold.free_parameter_list)
        if scale is None:
            scale=(0,1)
        self.order=order
        self.scale=scale
        self.par_ranges=GetRanges(mold.free_parameter_list,order=order)
    def __call__(self,array):
        # if type(array) is numpy.array:
            return NormalizeArray(array,self.par_ranges,scale=self.scale)
    def D(self,array):
        # if type(array) is numpy.array:
            return DenormalizeArray(array,self.par_ranges,scale=self.scale)