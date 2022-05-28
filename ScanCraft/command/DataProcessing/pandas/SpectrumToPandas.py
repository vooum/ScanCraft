#!/usr/bin/env python3

import numpy
from singledispatch import singledispatch

import pandas

from .. import SLHA_text,SLHA_document

from ...format.block_table import block_table
from ..DataOperators.list_operators import FlatToList

def _StringAccord(*index) -> str:
    '''
    Convert a tuple of (block_name,code) to a string of block_name_code.
    ('MASS',25) -> 'MASS_25'
    ('NMIX',(3,3)) -> 'NMIX_3_3'
    '''
    index=map(str,FlatToList(index))
    return '_'.join(index)

@singledispatch
def _DictAccord(index,spectrum)->dict:
    '''return all accords(block_code tuple) from index and its value.
    index can be:
    string of block name
    tuple of accord
    list of strings or tuples
    None: find all blocks
    '''
    print('correct the type of index')
    print(_DictAccord.__doc__)
    raise TypeError
@_DictAccord.register(tuple) # TUPLE
def _(index:tuple, spectrum:SLHA_text)->dict:
    accord_dict={_StringAccord(*index):spectrum(*index)}
    return accord_dict
@_DictAccord.register(str) # STRING
def _(index:str, spectrum:SLHA_text)->dict:
    block_dict=spectrum(index)
    accord_dict={}
    for key,value in block_dict.items():
        accord_dict[_StringAccord(index,key)]=value
    return accord_dict
@_DictAccord.register(list) # LIST
def _(index_list:list, spectrum:SLHA_text)->dict:
    accord_dict={}
    for index in index_list:
        accord_dict.update(_DictAccord(index,spectrum))
    return accord_dict
@_DictAccord.register(type(None)) # NONE
def _(index:None, spectrum:SLHA_text)->dict:
    # Get All READable blocks
    blocks=[b for b in spectrum.menu.keys()
            if hasattr( spectrum.block_format, str(b))]
    return _DictAccord(blocks,spectrum)

@singledispatch
def PandasSpectrum(spectrum:SLHA_text, index=None)-> pandas.Series: # SLHA object
    '''Collect information from SLHA_text object into a pandas.Series.
    spectrum can be:
        - SLHA_text object
        - path of SLHA file
        - list of these;
    index can be:
        - None, return all possible blocks
        - string, block name
        - tuple, block-code(-code) tuple
        - a list of string or tuple
    '''
    block_dict=_DictAccord(index,spectrum)
    return pandas.Series(block_dict)
@PandasSpectrum.register(str) # SLHA file path
def _(spectrum_path:str,index=None)->pandas.Series:
    return PandasSpectrum(SLHA_document(spectrum_path),index)
@PandasSpectrum.register(list) # LIST OF SLHA_text
def _(spectrum_list:list, index=None)->pandas.DataFrame:
    data_DF = pandas.DataFrame()
    for spectrum in spectrum_list:
        data_SR=PandasSpectrum(spectrum,index)
        data_DF=data_DF.append(data_SR ,ignore_index=True)
    return data_DF