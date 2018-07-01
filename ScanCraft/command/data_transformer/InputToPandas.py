#!/usr/bin/env python3
import numpy,pandas
from ..operators.iterable import FlatToList
# from ..format.data_container import capsule
from ..data_transformer.defult_parameter_order import defult_name_order
from ..scan.scan import scan
from ..color_print import Error

def InputToPandas(*point_list,order=None,title=None):
    if title is None: title='input'
    PL=FlatToList(point_list)
    flags=[(type(point) is scan) for point in PL]
    if not all(flags):
        print(flags)
        Error('wrong type when interpreting input data into Pandas')
    
    if order is None:
        order=defult_name_order(PL[0].free_parameter_list)

    par_array=[]
    for point in PL:
        array_row=[]
        for name in order:
            array_row.append(point.variable_list[name]())
        par_array.append(array_row)

    col=pandas.MultiIndex.from_tuples(
        [tuple([title,par.block,str(par.code),par.name])
            for par in [point.variable_list[n] for n in order]
        ],
        names=['title','block','code','name']
    )
    
    DF=pandas.DataFrame(numpy.array(par_array),columns=col)
    return DF