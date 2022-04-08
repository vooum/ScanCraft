#!/usr/bin/env python3

from .. import SLHA_text, SLHA_document
from ..DataOperators.list_operators import FlatToList
import numpy,pandas
from functools import singledispatch

@singledispatch
def _GetInitials(spectrum:SLHA_text) -> list(int):
    '''Get a list of initial PDGs from spectrum'''
    return [d for d in spectrum.menu.keys() if type(d) is int]

@_GetInitials.register(list)
def _(spectrum_list:list(SLHA_text)):
    '''Get lists of Decay initial PDGs from list of spectrums'''
    list_of_initials=[ _GetInitials(spec) for spec in spectrum_list ]
    all_initials=sorted( set( FlatToList(list_of_initials) ) )
    return all_initials


def _GetInitials(spectrum:SLHA_text)->list(int):
    '''Get a list of Decay initial PDGs'''
    initials = [d for d in spectrum.menu.keys() 
                if type(d) is int
            ]
    return initials

def _GetInitialList(spec_list:list(SLHA_text) )->list(int):
    '''a sorted list within all initial PDGs that may decay from all spectrums'''
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

def _GetAllFinals(spec_list:list[SLHA_text], initial:int)->list(tuple):
    '''Get all PDG tuples of final states of a given initial PDG'''
    list_of_finals=[ _GetFinals(spec,initial)
        for spec in spec_list
    ]
    final_list=sorted( set(
        FlatToList(list_of_finals)
    ))
    return final_list

def _ExpandDecayIndex(spec_list:list(SLHA_text), index:list) -> list:
    '''Expand index and its final PDG tuples to list of tuple( iniPDG, (final state PDGs) )
    the element of index should be:
        an integer, which is initial PDGs,
    or  a the tuple within an initial PDG and a tuple of final states PDGs'''
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

def _decay_index_To_String(in_fi:tuple) -> str:
    '''convert decay index: (iniPDG, (final_PDGs,) )
    to string: "DECAY_iniPDG->finalOne_finalTwo".'''
    return f'DECAY_{in_fi[0]}->{"_".join(in_fi[1])}'

def DecayToPandas(spectrum_list,index=None):
    '''Collect decay branch ratios of particles or channels in index.
    if index is None, collect decay of all particles;
    else the index should be a list. Its items can be
     - integer: all decay chennels of the particle which PDG is the integer;
     - tuple : ( ini_PDG, (final_PDGs) )
    '''
    SL=FlatToList(spectrum_list)
    # check all items in spectrum_list are SLHA_text objects
    flags=[isinstance(spec,SLHA_text) for spec in SL]
    assert all(flags), "wrong type when interpreting Decay data into Pandas"

    # get columns
    if index is None: ## Get columns from spectrum
        index=_GetInitialList(spectrum_list)
    elif type(index) is int:
        index=[index]
    elif isinstance(index,list):
        pass
    else:
        print('index of decay particle should be an integer, a list, or None.')
        exit()
    ini_final_list=_ExpandDecayIndex(SL,index) # [ ( iniPDG, (final state PDGs) ), ... ]
    column_Pd=map(_decay_index_To_String, ini_final_list)
    
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

LHA_path=str

def ReadDecayToPandas(LHA_files:list[LHA_path], index = None)-> pandas.DataFrame:
    '''Collect decay branch ratios of particles or channels in index from LHA files.
    if index is None, collect decay of all particles;
    else the index should be:
     - integer: all decay chennels of the particle which PDG is the integer;
     - tuple : ( ini_PDG, (final_PDGs) )
     - or a list of such tuples.
    This is another version of DecayToPandas which will READ spectrum_list one by one -- RAM will be saved.
    '''
    SL=FlatToList(LHA_files)
    # check all items in spectrum_list are SLHA_text objects
    flags=[isinstance(spec,str) for spec in SL]
    assert all(flags), "All items in LHA_files should be path like string of LHA files."

    decay_DataFrame=pandas.DataFrame()
    for spec in map(SLHA_document , SL):
        ini_final_list=_ExpandDecayIndex([spec],index) # [ ( iniPDG, (final state PDGs) ), ... ]
        data_dict={}
        for in_fi in ini_final_list:
            key=_decay_index_To_String(in_fi)
            data_dict[key]=spec('DECAY', ini, finals)
        decay_DataFrame=decay_DataFrame.append(data_dict,ignore_index=True)
    return decay_DataFrame
        
