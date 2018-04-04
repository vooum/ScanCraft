#!/usr/bin/env python3

from .SLHA import list_block,matrix_block

LOWEN={1:'BR(b->s_gamma)',11:'BR(b->s_gamma+Theor_Err)',12:'BR(b->s_gamma-Theor_Err)',
       2:'DeltaM_d_ps^-1',21:'DeltaM_d+Theor_Err',22:'DeltaM_d-Theor_Err',
       3:'DetaM_s',31:'DeltaM_s+Theor_Err',32:'DeltaM_s-Theor_Err',
       4:'BR(Bs->mu+mu-)',41:'BR(Bs->mu+mu-)+Theor_Err',42:'BR(Bs->mu+mu-)-Theor_Err',
       5:'BR(B+->tau+nu_tau)',51:'BR(B+->tau+nu_tau)+Theor_Err',52:'BR(B+->tau+nu_tau)-Theor_Err',
       6:'Del_a_mu',61:'Del_a_mu+Theor_Err',62:'Del_a_mu-Theor_Err'}

ABUNDANCE={}

NDMCROSSSECT={
    1:'csPsi',2:'csNsi',3:'csPsd',4:'csNsd'
}

ANNIHILATION={
}

REDCOUP={
}



class NMSSMTools_blocks():
    LOWEN=list_block(LOWEN)
    NDMCROSSSECT=list_block(NDMCROSSSECT)
    ANNIHILATION=list_block(ANNIHILATION)
    ABUNDANCE=list_block(ABUNDANCE)
    REDCOUP=matrix_block(REDCOUP)