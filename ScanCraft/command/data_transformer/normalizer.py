#!/usr/bin/env python3

import numpy
from .defult_parameter_order import input_parameter_list

def InputToUarray(*input_lists):
    pass



def PandasToUarray(data_frame,order=None,mode=None):
    if order is None:
        order=[i for i in input_parameter_list if i in mode.scalar_list.keys()]
        # order=[]
        # for name in input_parameter_list:
        #     if name in mode.scalar_list.keys():
        #         order.append(name)

    for name in order:
