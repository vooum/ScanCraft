#!/usr/bin/env python3

import re,copy,os
from .readline import *
import numpy as np
ParticalSpectrum={1:'d',2:'u',3:'s',4:'c',5:'b',6:'t',11:'e-',13:'muon',15:'tau',
	21:'gluon',23:'Z',25:'h1',35:'h2',36:'A1',45:'h3',46:'A2',
	1000011:'~e_L',1000012:'~nu_e_L',1000013:'~mu_L',1000014:'~nu_mu_L',1000015:'~tau_1',1000016:'~nu_tau_L',
	2000011:'~e_R',
	1000022:'N1',1000023:'N2',1000024:'C1',1000025:'N3',1000035:'N4',1000037:'C2',1000045:'N5',
	} 
def readfile(file):
    f=open(file,'r')
    spectr=f.readlines()
    f.close()
    omegafile=file.replace('spectr','omega')
    if os.path.isfile(omegafile):
        f=open(omegafile,'r')
        spectr+=f.readlines()
        f.close()
    
    global MinPar, ExtPar, Mh, Msp, b_phy, DM, Hmix, Nmix, Hcouplings, FT, LHCfit, Decay, HBresult, HSresult,Vacuum
    MinPar={}
    MinPar_n={0:'SCALE',1:'M0',2:'M12',3:'tanb',5:'A0'}
    ExtPar={}
    ExtPar_n={1:'M1',2:'M2',3:'M3'\
                ,11:'Atop',12:'Abotton',13:'Atau'\
                ,43:'MQ3',46:'MU3',49:'MB3'\
                ,61:'lambda',62:'kappa',63:'Alambda',64:'Akappa',65:'mu_eff'\
                ,124:'MA',125:'MP'}
    Mh={}
    Mh_n={25:'h1',35:'h2',45:'h3',36:'A1',46:'A2',37:'Ch'}
    Msp={}
    Msp_n={1000022:'N1',1000023:'N2',1000025:'N3',1000035:'N4',1000045:'N5',1000024:'C1',1000037:'C2'}
    b_phy={}
    b_phy_n={1:'b_sg',4:'b_mu'}
    DM={}
    DM_n={10:'DMRD',20:'s_Psi'}# other keys:LUX,csPsi,'csNsi','csPsd','csNsd'
    Hmix={}
    Hmix={'S':{},'P':{}}
    Nmix={}
    Hcouplings={}
    FT={}
    LHCfit={}
    LHCfit_n={1:'hrr',2:'hff',3:'hVV'}
    Decay={}
    HBresult=1
    HSresult=1.
    Vacuum='unknown'

    global MSQ2, MSU2, MSD2, MSL2, MSE2, TD, TE, TU
    MSQ2=np.zeros((3,3))
    MSU2=np.zeros((3,3))
    MSD2=np.zeros((3,3))
    MSL2=np.zeros((3,3))
    MSE2=np.zeros((3,3))
    TD=np.zeros((3,3))
    TE=np.zeros((3,3))
    TU=np.zeros((3,3))



    
    BLOCK=''
    DECAY=[]
    for line in spectr:
        a=readline(line)
        if type(a[0]) is str:
            if a[0].upper()=='DECAY':
                BLOCK=''
                DECAY=copy.deepcopy(a)
                Decay[DECAY[1]]={}
                continue
            if a[0].upper()=='BLOCK':BLOCK=a[1];DECAY=[];continue
        if BLOCK== 'SPINFO':
            if a[0] == 4: return False
            if a[0] == 3:
#                if True: return False
                if (#  re.search('# No Higgs in the',line)
                    re.search('Landau Pole',line)
                    or re.search('Relic density',line)
                    or re.search('micrOMEGAs',line)
                    or re.search('LUX',line)
                    or re.search('b -> s gamma',line)
                    or re.search('B_s -> mu+ mu-',line)
                    or re.search('Muon magn. mom.',line)
                    or re.search('Branching ratios of Higgs states < 1 GeV',line)
                    or re.search('M_H1^2<1',line)
                    or re.search('M_A1^2<1',line)
                    or re.search('b -> c tau nu',line)
                   ):pass
                else: return False
        elif BLOCK=='MINPAR':
            if a[0] in MinPar_n.keys():MinPar[MinPar_n[a[0]]]=a[1]
        elif BLOCK=='EXTPAR':
            if a[0] in ExtPar_n.keys():ExtPar[ExtPar_n[a[0]]]=a[1]
        elif BLOCK=='MASS':
            if a[0] in Mh_n.keys(): Mh['M_'+Mh_n[a[0]]]=a[1]
            elif a[0] in Msp_n.keys(): Msp['X_'+Msp_n[a[0]]]=a[1]
        elif BLOCK=='LOWEN':
            if a[0] in b_phy_n.keys(): b_phy[b_phy_n[a[0]]]=a[1]
            elif a[0] in DM_n.keys(): DM[DM_n[a[0]]]=a[1]
            elif a[0] == 'sigma(p)_SI': DM['LUX']=float(a[-2][:-2])
        elif BLOCK=='NMHMIX':
            if type(a[1]) is int: Hmix['S'][tuple(a[:2])]=a[2]
        elif BLOCK=='NMAMIX':
            if type(a[1]) is int: Hmix['P'][tuple(a[:2])]=a[2]
        elif BLOCK=='NMNMIX':
            if type(a[1]) is int: Nmix[tuple(a[:2])]=a[2]
        elif BLOCK=='REDCOUP':
            if type(a[1]) is int: Hcouplings[tuple(a[:2])]=a[2]
        elif BLOCK=='FINETUNING':
            if type(a[0]) is int: FT[a[0]]=a[1]
        elif BLOCK=='LHCFIT':
            if a[0] in LHCfit_n.keys(): LHCfit[LHCfit_n[a[0]]]=a[1]
        elif DECAY!=[] and a[-1]:
            if a[1]==2: Decay[DECAY[1]][tuple(a[2:4])]=a[0]
            elif a[1]==3: Decay[DECAY[1]][tuple(a[2:5])]=a[0]
        elif BLOCK=='HiggsBoundsResults':
            if a[0]==1:
                if a[1]==2:
                    HBresult=a[2]
        elif BLOCK=='HiggsSignalsResults':
            if a[0]==13:
                HSresult=a[1]
        # MSQ2, MSU2, MSD2, MSL2, MSE2, TD, TE, TU
        elif BLOCK=='MSQ2':
            if type(a[1]) is int: MSQ2[a[0]-1,a[1]-1]=a[2]
        elif BLOCK=='MSU2':
            if type(a[1]) is int: MSU2[a[0]-1,a[1]-1]=a[2]
        elif BLOCK=='MSD2':
            if type(a[1]) is int: MSD2[a[0]-1,a[1]-1]=a[2]
        elif BLOCK=='MSL2':
            if type(a[1]) is int: MSL2[a[0]-1,a[1]-1]=a[2]
        elif BLOCK=='MSE2':
            if type(a[1]) is int: MSE2[a[0]-1,a[1]-1]=a[2]
        elif BLOCK=='TD':
            if type(a[1]) is int: TD[a[0]-1,a[1]-1]=a[2]
        elif BLOCK=='TE':
            if type(a[1]) is int: TE[a[0]-1,a[1]-1]=a[2]
        elif BLOCK=='TU':
            if type(a[1]) is int: TU[a[0]-1,a[1]-1]=a[2]
        elif BLOCK=='NDMCROSSSECT':
            if a[-1]:DM[['CS','csPsi','csNsi','csPsd','csNsd'][a[0]]]=a[1]
        #elif BLOCK=='VEVACIOUSRESULTS':
            #if a[:2]==[0,0]: Vacuum=a[3]
        elif BLOCK=='HiggsSignalsPeakObservables':
            continue
    else:
        return True

if __name__ == "__main__":
#    exit()
    if readfile('mcmc/spectr0'):
        i=0
        for i in globals().keys():
            if type(eval(i)) is dict:
                print(i,eval(i))
#                eval('print('+i+')')
#                print(eval(i))
        print(HBresult,HSresult)
    else:print('excluded')
    
