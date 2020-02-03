#!/usr/bin/env python3

class LHC():
    '''Data from LHC,
    fromat: {name}=(central value , positive error, negative error)
    '''
    
    # Masses
    Higgs_mass=(125.10,0.14,0.14) # PDG-2019
    mh=HiggsMass

    # B physics
    b__s_gamma=(3.49e-4,0.19e-4,0.19e-4) # PDG-2019
    bsg=b__s_gamma

    b__d_gamma=(9.2e-6,3.0e-6,3.0e-6) # PDG-2019

    bs__mu_mu=(3.0e-9, .4e-9, .4e-9) # PDG-2019
    bmu=bs__mu_mu

    Z__h_a=(None,None,5.78e-3) #old