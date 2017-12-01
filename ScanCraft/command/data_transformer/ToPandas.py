#!/usr/bin/env python3
import numpy,pandas
from ..format.data_container import capsule
from .defult_parameter_order import input_parameter_list
from ..scan import scan
from ..color_print import Error

FlatList=lambda x: sum(map(FlatList,x),[]) if isinstance(x,(list,tuple)) else [x]

def CapsuleToPandas(capsule):
    pass

def InputToPandas(*point_list,order=None,title='input'):
    PL=FlatList(point_list)
    flags=[(type(point) is scan) for point in PL]
    if not all([type(point) is scan for point in PL]):
        print(flags)
        Error('wrong type when interpreting input data into Pandas')
    
    if order is None:
        order=[]
        for name in input_parameter_list:
            if name in PL[0].scalar_list.keys():
                order.append(name)

    par_array=[]
    for point in PL:
        array_row=[]
        for name in order:
            array_row.append(point.scalar_list[name]())
        par_array.append(array_row)

    col=pandas.MultiIndex.from_tuples(
        [tuple([title,par.block,par.code,par.name])
            for par in [point.scalar_list[n] for n in order]
        ],
        names=['title','block','code','name']
    )
    
    DF=pandas.DataFrame(numpy.array(par_array),columns=col)
    return DF