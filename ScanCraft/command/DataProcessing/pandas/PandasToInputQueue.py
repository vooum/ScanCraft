#!/usr/bin/env python3
import numpy,pandas

from ..format.data_structure_functions import FlatToList
from .defult_parameter_order import defult_name_order
from ..color_print import Error
from .ArrayToInputQueue import ArrayToInputQueue as A2Q
def PandasToInputQueue(DataFrame,mold):
    order=defult_name_order(mold.free_parameter_list)
    # col_tuple=[ t_i for t_i in DataFrame.columns]
    arrange=[]
    for name in order:#search name in columns
        seat=None
        for i, t_i in enumerate(DataFrame.columns):#search with name level
            if name==t_i[3]:
                seat=i
                break
        else:# search with block & code levels
            for i, t_i in enumerate(DataFrame.columns):
                if t_i[1] in mold.block_list.keys():
                    if t_i[2] in mold.block_list[t_i[1]]:
                        seat=i
                        break
            else:#still not found
                Error('"%s" not match any columns in the data frame'%name)
        if seat is None:#check
            Error('%s not found and logic error, check the function PandasToInputQueue'%name)
        else:
            arrange.append(seat)
    array=DataFrame.values[:,arrange]
    q=A2Q(array,mold,order=order)
    return q