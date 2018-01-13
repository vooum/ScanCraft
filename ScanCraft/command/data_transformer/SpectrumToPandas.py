#!/usr/bin/env python3

import numpy,pandas
from ..format.data_container import capsule
from ..color_print import Error
from ..format.block_table import block_table

from ..format.data_structure_functions import FlatToList
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
    for b_name in sorted(SL[0].__dict__.keys()):
        #c_i=[title]
        b_dict=getattr(SL[0],b_name)
        if type(b_dict) is not dict:continue
        for code in sorted(b_dict.keys()):
            # if isinstance(code,(tuple,list)):
            #     c_i[2]=repr(code)
            # if hasattr(block_table,b_name):
            try:
                c_i=[title,b_name,repr(code),getattr(block_table,b_name)(code)]
            except KeyError:
                continue
            except AttributeError:
                continue
            else:
                column_list.append(tuple(c_i))
                block_code_list.append((b_name,code))
    column_Pd=pandas.MultiIndex.from_tuples(column_list
                                            ,names=['title','block','code','name']
                                            )
    # get data as array
    value_list=[]
    for spec in SL:
        row=[]
        for b_name,code in block_code_list:
            row.append(getattr(spec,b_name)[code])
        value_list.append(row)
    # generate dataframe
    DF=pandas.DataFrame(numpy.array(value_list),columns=column_Pd)
    return DF