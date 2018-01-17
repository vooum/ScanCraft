#!/usr/bin/env python3
# Not Finished
import pandas,numpy
from .classify import Classify
from .calculate import Calculate
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
        elif type(calculate_model) is Calculate:
            self.Calculate=calculate_model
        self.mold=mold
        self.data_range=GetRanges(mold.free_parameter_list)
        self.excluded=numpy.array([])
        self.accepted=numpy.array([])
    def SetData(self,accepted_points=None,spectrums=None,excluded_points=None):
        if accepted_points is not None:
            pass