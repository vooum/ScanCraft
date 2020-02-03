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
        return (prediction-self.value)**2/self.variance

class Chisquare_Test():
    mh=X2(LHC.Higgs_mass,err_th=mh_error_th)
    bsg=X2(LHC.b__s_gamma)
    bmu=X2(LHC.bs__mu_mu)
    omg=X2(dark_matter.relic_density,err_th=omg_err_th)

def Chisq(**predictions):
    X2_dict={}
    for key,prediction in predictions.items():
        X2_dict[key]=getattr(Chisquare_Test,key)(prediction)
    return X2_dict