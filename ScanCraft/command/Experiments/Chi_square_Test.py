#!/usr/bin/env python3

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
#    InterpolatePsd=dark_matter.direct_detection.Psd
#    InterpolatePsi=dark_matter.direct_detection.Psi
#    InterpolateNsd=dark_matter.direct_detection.Nsd
    def __init__(self,Interpolate):
        self.Interpolate=Interpolate
        self.mass=Interpolate.x
        self.limit=Interpolate.y
    def __call__(self,mass,cross_section):
        limit=self.Interpolate(mass)
        delta_sigmasq=limit**2/1.64**2+(0.2*cross_section)**2
        chisquare=cross_section**2/delta_sigmasq
        return chisquare

class Chisquare_Test():
    mh=X2(LHC.Higgs_mass,err_th=mh_error_th)
    bsg=X2(LHC.b__s_gamma)
    bmu=X2(LHC.bs__mu_mu)
    omg=X2(dark_matter.relic_density,err_th=omg_err_th)
    Psd=DMDD_X2(dark_matter.direct_detection.Psd)
    Psi=DMDD_X2(dark_matter.direct_detection.Psi)
    Nsd=DMDD_X2(dark_matter.direct_detection.Nsd)

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