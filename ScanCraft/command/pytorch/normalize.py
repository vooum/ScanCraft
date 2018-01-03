#!/usr/bin/env python3

import numpy
from ..data_transformer.defult_parameter_order import defult_name_order
from ..data_transformer.InputListToPandas import InputListToPandas
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
        
def NormalizePointListToPandas(point_list,order=None,title=None):
    if order is None:
        order=defult_name_order(point_list[0].free_parameter_list)
    if title is None:
        title='normalized'
    par_ranges=GetRanges(point_list[0].free_parameter_list,order=order)
    raw=InputListToPandas(point_list,order=order,title=title)
    normalized=(raw-par_ranges[0])/(par_ranges[1]-par_ranges[0])
    return normalized

def DenormalizeUniform(array,mold,order=None):
    if order is None:
        order=defult_name_order(mold.free_parameter_list)
    par_ranges=GetRanges(mold.free_parameter_list,order=order)
    array=array*(par_ranges[1]-par_ranges[0])+par_ranges[0]
    return array