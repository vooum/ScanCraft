#!/usr/bin/env python3

import numpy,pandas
#from multiprocessing import Pool 
from .. import SLHA_text
from ...format.block_table import block_table
from ...operators.iterable import FlatToList,SortMixList
red='\x1b[38;5;1m'
bold='\x1b[1m'
clean_color='\x1b[0m'

def _GetBlocks(spectrum:SLHA_text) -> list:
    '''Get a list of READable block names of a given spectrum
    '''
    readable_blocks=[b for b in spectrum.block_dict.keys() 
                        if hasattr( spectrum.block_format, b)
                    ]
    return readable_blocks
def _GetBlockList(spec_list):
    '''Get a list of All block names from a list of spectrum'''
    # with Pool() as P:
    #     block_lists=P.map( _GetBlocks, spec_list )
    block_lists=[_GetBlocks(spec) for spec in spec_list]
    block_set=set(FlatToList(block_lists))
    block_list=[ b for b in dir(block_table) 
                    if b in block_set
                ]
    return block_list
def _GetCodes(spectrum,block_name)->list:
    '''Get a list of codes of given spectrum and block_name'''
    return list(spectrum(block_name).keys())
    # return list( pars[0](pars[1]).keys() )
def _GetCodeList(spec_list,block_name):
    '''Collect codes of given block_name from all spectrums in spec_list'''
    # with Pool() as P:
    #     code_lists=P.map(
    #         _GetCodes,
    #         [(spec,block_name) for spec in spec_list]
    #     )
    code_lists=[_GetCodes(spec,block_name) for spec in spec_list]
    code_list=list(set(
        sum(code_lists,[])
    ))
    code_list.sort()
    return code_list
def _ExpandIndex(spec_list,index):
    '''Expand index (block_name or a list of it) to tuples of (block_name, code)'''
    tuple_block_code_list=[]
    for i_i in index:
        if type(i_i) is str: # block_name
            tuple_block_code_list.extend(
                [ (i_i,code) for code in _GetCodeList(spec_list,i_i)]
            )
        elif type(i_i) is tuple: # (block_name,code)
            tuple_block_code_list.append(i_i)
    return tuple_block_code_list

def SpectrumToPandas(*spectrum_list,index=None,title=None):
    if title is None: title='spectrum'
    SL=FlatToList(spectrum_list)
    # check all items in spectrum_list are SLHA_text objects
    flags=[isinstance(spec,SLHA_text) for spec in SL]
    if not all(flags):
        print(flags.index(False))
        print(f'{red}{bold}wrong type when interpreting spectrum data into Pandas{clean_color}')
        exit()
    # get columns
    column_list=[]
    block_code_list=[]
    # get columns from spectrum
    if index is None:# Not done
        index=_GetBlockList(SL)
    elif type(index) is str:
        index=[index]
    elif isinstance(index,list):
        pass
    else:
        print(f'{red}{bold}Wrong type of index.{clean_color}')
        exit()
    
    block_code_list=_ExpandIndex(SL,index)
    column_list=[
        ( title,b,repr(c),getattr(block_table,b)(c,default='unknown') )
        for b,c in block_code_list
    ]
    
    # for index_i in index:
    #     codes=list(set( # codes for given BLOCK
    #         sum([
    #             list(S_i(b_name).keys()) for S_i in SL
    #         ], [] )
    #     )).sort()
    #     for code in codes:
    #         column_list.append(tuple([
    #             title,b_name,repr(code),getattr(block_table,b_name)(code,default='unknown')
    #         ]))
    #         block_code_list.append( (b_name,code) )

    column_Pd=pandas.MultiIndex.from_tuples(column_list 
                                            ,names=['title','block','code','name']
                                            )
    # get data as array
    value_list=[]
    for spec in SL:
        row=[]
        for b_name,code in block_code_list:
            # row.append(getattr(spec,b_name,{}).get(code,numpy.nan))
            try:
                row.append( spec(b_name,code) )
            except KeyError:
                row.append(numpy.nan)
        value_list.append(row)
    widths=set([len(row) for row in value_list])
    # print('width=',widths)
    # generate dataframe
    DF=pandas.DataFrame(numpy.array(value_list),columns=column_Pd)
    return DF