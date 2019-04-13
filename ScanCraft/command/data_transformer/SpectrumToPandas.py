#!/usr/bin/env python3

import numpy,pandas
from ..format.data_container import capsule
from ..color_print import Error
from ..format.block_table import block_table
from ..operators.iterable import FlatToList,SortMixList
def SpectrumToPandas(*spectrum_list,title=None):
    if title is None: title='spectrum'
    SL=FlatToList(spectrum_list)
    flags=[(type(spec)is capsule) for spec in SL]
    if not all(flags):
        print(flags)
        Error('wrong type when interpreting spectrum data into Pandas')

    # get column
    column_list=[]
    block_code_list=[]
    b_name_list=list(set(FlatToList([list(S_i.__dict__.keys()) for S_i in SL])))
    for b_name in sorted([i for i in b_name_list if hasattr(block_table,i)]):
        code_list_b=list(set(sum([list(getattr(S_i,b_name,{}).keys()) for S_i in SL],[])))
        for code in SortMixList(code_list_b):
            column_list.append(tuple([title,b_name,repr(code),getattr(block_table,b_name)(code,default='unknown')]))
            block_code_list.append((b_name,code))

    column_Pd=pandas.MultiIndex.from_tuples(column_list 
                                            ,names=['title','block','code','name']
                                            )
    # get data as array
    value_list=[]
    for spec in SL:
        row=[]
        for b_name,code in block_code_list:
            row.append(getattr(spec,b_name,{}).get(code,numpy.nan))
        value_list.append(row)
    widths=set([len(row) for row in value_list])
    # print('width=',widths)
    # generate dataframe
    DF=pandas.DataFrame(numpy.array(value_list),columns=column_Pd)
    return DF