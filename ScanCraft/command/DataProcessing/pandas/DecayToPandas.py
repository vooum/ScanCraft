#!/usr/bin/env python3

from .. import SLHA_text, SLHA_document
import pandas
from functools import singledispatch

def _GetInitials(spectrum:SLHA_text) -> list:
    '''Get a list of all possible decay initial particle PDGs from a spectrum
    when initial particle is not given.'''
    return [d for d in spectrum.menu.keys() if type(d) is int]
    # like: [24, 25, ...]

# One spectrum
# initial can be:
#  - None, which means all initial particles
#  - an integer, which is initial particle PDG
#  - a list of initial particle PDGs
#  - a list of channel tuples (initial_PDG, tuple(final_PDGs))
@singledispatch
def _Get_channel_list(initial:int, spectrum:SLHA_text ) -> list:
    # Initial PDG is given
    '''Get a list:
    start with decay WIDTH of a particle specified by PDG,
    then all its decay channels: tuple( iniPDG, (final state PDGs) )
    from a spectrum'''
    channel_list = [(initial, 'WIDTH')]
    finals=[ f for f in spectrum('DECAY',initial).keys() if type(f) is tuple ]
    channel_list.extend( [ (initial,f) for f in finals ] )
    return channel_list
@_Get_channel_list.register(tuple)
def _(channel:tuple, spectrum:SLHA_text):
    return [channel]
@_Get_channel_list.register(list)
def _(initial:list, spectrum:SLHA_text):
    channel_list=sum( # sum lists
        [ _Get_channel_list(ini,spectrum) for ini in initial ],
        [] )
    return channel_list
@_Get_channel_list.register(type(None))
def _(initial:None, spectrum:SLHA_text):
    return _Get_channel_list(_GetInitials(spectrum) ,spectrum)

def _StringChannel(channel:tuple) -> str:
    '''convert decay index: (iniPDG, “WIDTH” or (final_PDGs,) )
    to string: "DECAY_iniPDG->finalOne_finalTwo".'''
    ini,finals=channel
    if finals=='WIDTH':
        return f'DECAY_{ini}_WIDTH'
    elif type(finals) is tuple:
        final_str="_".join( [str(fi) for fi in finals] )
        return f'DECAY_{ini}->{final_str}'

@singledispatch
def _DictDecay(spectrum:SLHA_text, initial=None)->dict:
    decay_dict={}
    channel_list=_Get_channel_list(initial,spectrum)
    for channel in channel_list:
        key=_StringChannel(channel)
        decay_dict[key]=spectrum('DECAY',*channel)
    return decay_dict
@_DictDecay.register(str)
def _(spectrum:str, initial=None):
    return _DictDecay(SLHA_document(spectrum),initial)

@singledispatch
def PandasDecay(spectrum:SLHA_text, initial=None)->pandas.Series:
    '''Collect decay branch ratios of initial particles.
    initial can be:
        - None, which means all initial particles
        - an integer, which is initial particle PDG
        - a list of initial particle PDGs
    '''
    decay_dict=_DictDecay(spectrum,initial)
    return pandas.Series(decay_dict)
@PandasDecay.register(list)
def _(spectrum_list:list, initial=None)->pandas.DataFrame:
    data_DF=pandas.DataFrame()
    for spectrum in spectrum_list:
        decay_dict=_DictDecay(spectrum,initial)
        data_DF = data_DF.append(decay_dict,ignore_index=True)
    return data_DF