#!/usr/bin/env python3
import os,numpy
from .colliders import Exp_data
from scipy.interpolate import interp1d

def _GetInterpolation(file_name):
    Dir=os.path.dirname(__file__)
    mass,limit=numpy.loadtxt(os.path.join(Dir,file_name),unpack=True,comments='#',delimiter=',')
    interpolation=interp1d(mass,limit,fill_value="extrapolate")
    return interpolation

class _DMDD():
    # Psi_Xenon1T_2017=_GetInterpolation('Xenon1T_2017.csv')
    # Psd_PandaX_2016=_GetInterpolation('PandaX_Psd_2016.txt')
    # Nsd_PandaX_2016=_GetInterpolation('PandaX_Nsd_2016.txt')
    Psi_Xenon1T_2018=_GetInterpolation('Xenon1T_2018_Psi.csv')
    Psd_Xenon1T_2019=_GetInterpolation('Xenon1T_2019_Psd.csv')
    Nsd_Xenon1T_2019=_GetInterpolation('Xenon1T_2019_Nsd.csv')
    #
    Psi=Psi_Xenon1T_2018
    Psd=Psd_Xenon1T_2019
    Nsd=Nsd_Xenon1T_2019

class dark_matter():
    relic_density=Exp_data(0.1187,0.,0.)
    # DD upper limit
    direct_detection=_DMDD