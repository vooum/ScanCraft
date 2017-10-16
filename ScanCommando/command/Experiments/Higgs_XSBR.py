#! /usr/bin/env python3
import os
import numpy
from scipy.interpolate import interp1d

def GetCS(file_name):
    return  numpy.loadtxt(file_name,
                usecols=(0,1),
            )

def interp_XS(file_name):
    data=GetCS(os.path.join(os.path.dirname(__file__),'Higgs_XSBR',file_name))
    mass=data[:,0]
    CS=data[:,1]
    return interp1d(mass,CS,fill_value='extrapolate')

class Higgs_XS():
    ggF=interp_XS('Higgs_CS_BSM_13TeV_ggF.txt')
    ttH=interp_XS('Higgs_CS_BSM_13TeV_ttH.txt')
    VBF=interp_XS('Higgs_CS_BSM_13TeV_VBF.txt')
    ZH =interp_XS('Higgs_CS_BSM_13TeV_ZH.txt')
    WH =interp_XS('Higgs_CS_BSM_13TeV_WH.txt')
    