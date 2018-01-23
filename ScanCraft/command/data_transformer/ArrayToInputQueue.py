#!/usr/bin/env python3
import copy,queue
from .defult_parameter_order import input_parameter_list
# from ..format.data_structure_functions import FlatToList
def ArrayToInputQueue(array,mold,order=None,q=None):
    if order==None:
        # free_par_namelist=FlatToList(mold.scalar_list,mold.matrix_list)
        # print(free_par_namelist)
        name_list=[pname for pname in input_parameter_list if pname in mold.scalar_list.keys()]
        # print(name_list)
    if q==None:
        q=queue.Queue(100000)
    for row in array:
        point=copy.deepcopy(mold)
        for name,value in zip(name_list,row):
            point.scalar_list[name].value=value
        for fix in point.follower_list.values():
            fix.Generate()
            # print(name,value)
        q.put(point)
    return q
