#!/usr/bin/env python3
import os
import numpy

from .experimental_data.colliders import LHC
from .experimental_data.dark_matter import dark_matter

mh_error_th=3.
omg_err_th=0.1*dark_matter.relic_density.central_value

class X2():
    def __init__(self,data,err_th=0):
        self.value=data.central_value
        self.err=(data.positive_error+err_th,data.negative_error+err_th)
        self.variance=(self.err[0]**2+self.err[1]**2)/2.
    def __call__(self,prediction):
        chisquare= (prediction-self.value)**2/self.variance
        return chisquare

class DMDD_X2():
    def __init__(self,Interpolate):
        self.Interpolate=Interpolate
        self.mass=Interpolate.x
        self.limit=Interpolate.y
    def __call__(self,mass,cross_section):
        limit=self.Interpolate(mass)
        delta_sigmasq=limit**2/1.64**2+(0.2*cross_section)**2
        chisquare=cross_section**2/delta_sigmasq
        return chisquare

def chi2_CP(xz,xw,xb,xt,xtau,xg,xj):
    '''
    Author:yuanfang
    pars:xz,xw,xb,xt,xtau,xg,xj are couplings
    Notes:calculate higgs coupling chi2 with correlation matrix
    addapted from junjie cao
    Ref:
    ATLAS-CONF-2019-005
    '''
    rho=numpy.array([
        [1, 0.46, 0.24, 0.66, 0.34, 0.52, 0.39], 
        [0.46, 1, 0.16, 0.51, 0.38,0.57, 0.06],
        [0.24, 0.16, 1, 0.41, 0.10, 0.12, 0.43],
        [0.66, 0.51,0.41, 1, 0.46, 0.62, 0.73],
        [0.34, 0.38, 0.10, 0.46, 1, 0.47,0.27],
        [0.52, 0.57, 0.12, 0.62, 0.47, 1, 0.17], 
        [0.39, 0.06, 0.43,0.73, 0.27, 0.17, 1]
        ],dtype=numpy.float64)

    err = numpy.array([0.08, 0.09, 0.18, 0.15, 0.16, 0.09, 0.11])

    kk=numpy.zeros((7,7))
    for i in range(7):
        for j in range(7):
            kk[i,j]=err[i]*rho[i,j]*err[j]
    #print('kk={}\n'.format(kk))

    Xs=numpy.array([
        xz-1.11,
        xw-1.05,
        xb-1.03,
        xt-1.09,
        xtau-1.05,
        xg-1.05,
        xj-0.99
        ])
    chi2=Xs.dot(numpy.linalg.inv(kk)).dot(Xs)
    return chi2

class Chisquare_Test():
    mh=X2(LHC.Higgs_mass,err_th=mh_error_th)
    bsg=X2(LHC.b__s_gamma)
    bmu=X2(LHC.bs__mu_mu)
    relic=X2(dark_matter.relic_density,err_th=omg_err_th)
    Psd=DMDD_X2(dark_matter.direct_detection.Psd)
    Psi=DMDD_X2(dark_matter.direct_detection.Psi)
    Nsd=DMDD_X2(dark_matter.direct_detection.Nsd)
    Higgs_coupling=chi2_CP


def Chisq(**predictions):
    X2_dict={}
    for key,prediction in predictions.items():
        input_type=type(prediction)
        if input_type is float:
            X2_dict[key]=getattr(Chisquare_Test,key)(prediction)
        elif input_type in [list,tuple]:
            X2_dict[key]=getattr(Chisquare_Test,key)(*prediction)
        elif input_type is dict:
            X2_dict[key]=getattr(Chisquare_Test,key)(**prediction)
    return X2_dict