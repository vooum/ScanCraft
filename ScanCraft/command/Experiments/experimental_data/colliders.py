#!/usr/bin/env python3
from collections import namedtuple

Exp_data=namedtuple('experimental_data',['central_value','positive_error','negative_error'])

class LHC():
    '''Data from LHC,
    '''
    # Masses
    Higgs_mass=Exp_data(125.10,0.14,0.14) # PDG-2019

    # B physics
    b__s_gamma=Exp_data(3.49e-4,0.19e-4,0.19e-4) # PDG-2019

    b__d_gamma=Exp_data(9.2e-6,3.0e-6,3.0e-6) # PDG-2019

    bs__mu_mu=Exp_data(3.0e-9, .4e-9, .4e-9) # PDG-2019

    Z__h_a=(None,None,5.78e-3) #old