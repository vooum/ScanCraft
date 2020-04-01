#!/usr/bin/env python3
import os,numpy
from scipy.interpolate import interp1d
from .colliders import LHC
from ..color_print import Error
def GetInterpolation(file_name):
    Dir=os.path.dirname(__file__)
    m,l=numpy.loadtxt(os.path.join(Dir,file_name),unpack=True)
    if file_name=='Xenon1T_2017.txt':l*=1e-45
    interpolation=interp1d(m,l)
    return interpolation

class DMDD():
    Psi=GetInterpolation('Xenon1T_2017.txt')
    Psd=GetInterpolation('PandaX_Psd_2016.txt')
    Nsd=GetInterpolation('PandaX_Nsd_2016.txt')

def Chisqure(**obs):
    chi_list={}
    for exp,value in obs.items():
        if hasattr(LHC,exp):
            center,up,down=getattr(LHC,exp)
            X2=(center-value)**2/(up**2+down**2)
            chi_list[exp]=X2
        else:
            Error('%s not found'%exp)
    return chi_list

def constraints(**obs):
    pass_list={}
    for exp,value in obs.items():
        pass_const=False
        if exp=='mh':
            if (value>122.09) and (value<128.09):
                pass_const=True
        if hasattr(LHC,exp):
            center,up,down=getattr(LHC,exp)
            if (value<center+2*up) and (value>center-2*down):
                pass_const=True
        else:
            Error('%s not found'%exp)
        pass_list[exp]=pass_const
    return pass_list