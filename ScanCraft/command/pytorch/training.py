#!/usr/bin/env python3

from .classify import Classify
from .normalize import GetRanges
from ..format.data_container import capsule
from ..scan.scan import scan

class Training():
    def __init__(self,mold,model=None):
        if type(model) is str:
            self.Classify=torch.load(model)
        elif type(model) is Classify:
            self.Classify=model
        self.mold=mold
        self.data_range=GetRanges(mold.free_parameter_list)
    def AddData(self,input_points,spectrums):
