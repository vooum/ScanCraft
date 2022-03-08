#!/usr/bin/env python3

from .. import SLHA_text
from ..DataOperators.list_operators import FlatToList
import numpy,pandas

def _GetInitials(spectrum:SLHA_text)->list(int):
    '''Get a list of Decay initial PDGs'''
    initials = [d for d in spectrum.menu.keys() 
                if type(d) is int
            ]
    return initials

def _GetInitialList(spec_list:list(SLHA_text) )->list(int):
    '''a sorted list within all initial PDG that may decay'''
    # only used when initial particle is not assigned
    list_of_initials=[
        _GetInitials(spec) for spec in spec_list
    ]
    initial_list=sorted( set(
        FlatToList(list_of_initials)
    ))
    return initial_list

def _GetFinals(spectrum:SLHA_text,initial:int) -> list(tuple):
    '''Get a list of final states tuples for a given initial PDG'''
    return list( spectrum('DECAY',initial).keys() )

def _GetAllFinals(spec_list:list(SLHA_text),initial:int)->list(tuple):
    '''Get all PDG tuples of final states of a given initial PDG'''
    list_of_finals=[ _GetFinals(spec)
        for spec in spec_list
    ]
    final_list=sorted( set(
        FlatToList(list_of_finals)
    ))
    return final_list

def _ExpandDecayIndex(spec_list:list(SLHA_text), index:list) -> list:
    '''Expand index and its final PDG tuples to list of tuple( iniPDG, (final state PDGs) )
    the element of index should be an integer, 
    or a the tuple within an initial PDG and a tuple of final states PDGs'''
    tuple_ini_final_list=[]
    for ini in  index:
        if type(ini) is int: #Decay particle PDG
            tuple_ini_final_list.extend(
                [ (ini,finals) for finals in _GetAllFinals(spec_list,ini) ]
            )
        elif type(ini) is tuple:
            # a tuple of ( iniPDG, (final states tuple))
            assert len(ini)==2, "Index element should be an integer or a lenth 2 tuple."
            assert type(ini[1]) is tuple, "Second index element should be a tuple of final states PDGs"
            tuple_ini_final_list.append(ini)
    return tuple_ini_final_list

def DecayToPandas(*spectrum_list,index=None,title='Decay'):
    '''Collect decay branch ratios of particles or channels in index.
    if index is None, collect decay of all particles;
    else the index should be a list. Its items can be
     - integer: all decay chennels of the particle which PDG is the integer;
     - tuple
    '''
    SL=FlatToList(spectrum_list)
    # check all items in spectrum_list are SLHA_text objects
    flags=[isinstance(spec,SLHA_text) for spec in SL]
    assert all(flags), "wrong type when interpreting Decay data into Pandas"
    # get columns
    column_list=[]
    block_code_list=[]
    ## Get columns from spectrum
    if index is None:
        index=_GetInitialList(spectrum_list)
    elif index is int:
        index=index
    elif isinstance(index,list):
        pass
    else:
        print('index of decay particle should be an integer, a list, or None.')
        exit()
    
    # [ ( iniPDG, (final state PDGs) ), ... ]
    ini_final_list=_ExpandDecayIndex(SL,index)

    column_list=[
        (title, ini, finals, f'{ini}->{finals}' )
        for ini, finals in ini_final_list
    ]
    # pandas column
    column_Pd=pandas.MultiIndex.from_tuples(column_list 
                ,names=['title','block','code','name']
                )
    
    # get data array
    value_list = []
    for spec in SL:
        row=[]
        for ini, finals in ini_final_list:
            try:
                row.append(spec('DECAY', ini, finals) )
            except KeyError:
                row.append(numpy.nan)
        value_list.append(row)
    DF=pandas.DataFrame(numpy.array(value_list),columns=column_Pd)
    return DF