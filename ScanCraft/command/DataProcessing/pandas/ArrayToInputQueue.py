#!/usr/bin/env python3
import copy,queue
# from ..format.data_structure_functions import FlatToList
from ..data_transformer.defult_parameter_order import defult_name_order
def ArrayToInputQueue(array,mold,order=None,q=None):
    if order==None:
        # free_par_namelist=FlatToList(mold.scalar_list,mold.matrix_list)
        # print(free_par_namelist)
        order=defult_name_order(mold.free_parameter_list)
        # print(order)
    if q==None:
        q=queue.Queue()
    for row in array:
        point=copy.deepcopy(mold)
        for name,value in zip(order,row):
            point.free_parameter_list[name].value=value
        # for follower in point.follower_list.values():
        #     follower.Generate()
            # print(name,value)
        q.put(point)
    return q
