#!/usr/bin/env python3

from .classify import Classify
from .normalize import GetRanges
from ..format.data_container import capsule
from ..scan.scan import scan

class Training():
    def __init__(self,mold,classify_model=None,calculate_model=None):
        if type(classify_model) is str:
            self.Classify=torch.load(classify_model)
        elif type(classify_model) is Classify:
            self.Classify=model
        if type(calculate_model) is str:
            self.Calculate=torch.load(calculate_model)
        elif type(calculate_model) is 
        self.mold=mold
        self.data_range=GetRanges(mold.free_parameter_list)
    def AddData(self,input_points,spectrums):
