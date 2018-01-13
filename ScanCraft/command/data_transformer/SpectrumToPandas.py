#!/usr/bin/env python3

import numpy,pandas
from ..format.data_container import capsule

from ..format.data_structure_functions import FlatToList
def SpectrumToPandas(*spectrum_list,title=None):
    if title is None: title='spectrum'
    SL=FlatToList(spectrum_list)
    flags=[(type(spec)is capsule) for spec in SL]
    if not all(flags):
        