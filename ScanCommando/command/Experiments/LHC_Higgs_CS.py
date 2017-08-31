#! /usr/bin/env python3
import os
import numpy
from scipy.interpolate import interp1d

def GetCS(file_name):
    return  numpy.loadtxt(file_name,
                usecols=(0,1),
                #converters=lambda x:float(x[1:]) #dict.fromkeys( [2,3,4,5,6], lambda x:float(x[1:]) )
            )

#print(GetCS('Higgs_CS_BSM_13TeV_ggF.txt'))
#print(GetCS('Higgs_CS_BSM_13TeV_vbf.txt'))

def Higgs_CS(file_naame):
    data=GetCS(os.path.join(os.path.dirname(__file__),file_naame))
    mass=data[:,0]
    CS=data[:,1]
    return interp1d(mass,CS,bounds_error=True)