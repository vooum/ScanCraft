#!/usr/bin/env python3
import os
from .readline import *

ParticleSpectrum={
    1:'d',2:'u',3:'s',4:'c',5:'b',6:'t',
    11:'e-',12:'nu_e',13:'muon',14:'nu_mu',15:'tau',16:'nu_tau',
    21:'gluon',22:'r',23:'Z',24:'W',
    25:'h1',35:'h2',36:'A1',37:'C1',45:'h3',46:'A2',
    1000001:'Sd_L',1000002:'Su_L',1000003:'Ss_L',1000004:'Sc_L',1000005:'Sb_1',1000006:'St_1',
    2000001:'Sd_R',2000002:'Su_R',2000003:'Ss_R',2000004:'Sc_R',2000005:'Sb_2',2000006:'St_2',
	1000011:'Se_L',1000012:'Snu_e_L',1000013:'Smu_L',1000014:'Snu_mu_L',1000015:'Stau_1',1000016:'Snu_tau_L',
	2000011:'Se_R',2000013:'Smu_R',2000015:'Stau_2',
    1000021:'Sg',
	1000022:'N1',1000023:'N2',1000024:'C1',1000025:'N3',1000035:'N4',1000037:'C2',1000045:'N5',
	}

def GetName(NameTuple):
    name=[]
    for i in NameTuple:
        if i>0:
            name.append(ParticleSpectrum[i])
        elif i<0:
            name.append('-'+ParticleSpectrum[-i])
    return '&'.join(name)

class translate:
    def __init__(self,DecayList):
        self.width={}
        for id in DecayList.keys():
            setattr(self,ParticleSpectrum[id],{})
            init=getattr(self,ParticleSpectrum[id])
            for outS, outR in DecayList[id].items():
                if type(outS) is str:
                    self.width[ParticleSpectrum[id]]=outR
                else:
                    init[GetName(outS)]=outR
        return



class readBLOCK:
    def InBlock(self):
        if self.lines[self.i][:5].upper() == 'BLOCK':
            return False
        else:
            self.a=readline(self.lines[self.i])
            self.i+=1
            return True

    def readSPINFO(self):
        self.PROB=[]
        while self.InBlock():
            if self.a[0]==4:
                self.p=False
                return
            elif self.a[0]==3:
                for Key in self.discount:
                    if Key in self.a[1]:
                        break
                else:
                    self.PROB.append(self.a[1])
        return

    def readMINPAR(self):
        self.MINPAR={}
        self.MinPar={}
        MinPar_n={0:'SCALE',1:'M0',2:'M12',3:'tanB',5:'A0'}
        while self.InBlock():
            if type(self.a[0]) is int:
                self.MINPAR[self.a[0]]=self.a[1]
            if self.a[0] in MinPar_n.keys():
                self.MinPar[MinPar_n[self.a[0]]]=self.a[1]
        return
    
    def readEXTPAR(self):
        self.EXTPAR={}
        self.ExtPar={}
        ExtPar_n={1:'M1',2:'M2',3:'M3'\
                ,11:'Atop',12:'Abotton',13:'Atau'\
                ,43:'MQ3',46:'MU3',49:'MB3'\
                ,61:'Lambda',62:'Kappa',63:'Alambda',64:'Akappa',65:'mu_eff'\
                ,124:'MA',125:'MP'}
        while self.InBlock():
            self.EXTPAR[self.a[0]]=self.a[1]
            if self.a[0] in ExtPar_n.keys():
                self.ExtPar[ExtPar_n[self.a[0]]]=self.a[1]
        return

    def readMASS(self):
        self.MASS={}
        self.Mh={}
        Mh_n={25:'h1',35:'h2',45:'h3',36:'A1',46:'A2',37:'Ch'}
        self.Msp={}
        Msp_n={1000022:'N1',1000023:'N2',1000025:'N3',1000035:'N4',1000045:'N5',1000024:'C1',1000037:'C2'}
        while self.InBlock():
            if self.a[-1]:self.MASS[self.a[0]]=self.a[1]
            if self.a[0] in Mh_n.keys():
                self.Mh['M_'+Mh_n[self.a[0]]]=self.a[1]
            elif self.a[0] in Msp_n.keys():
                self.Msp['X_'+Msp_n[self.a[0]]]=self.a[1]
        return
    
    def readLOWEN(self):
        self.b_phy={}
        b_phy_n={1:'b_sg',4:'b_mu'}
        self.DM={}
        DM_n={10:'DMRD',20:'s_Psi'}
        while self.InBlock():
            if self.a[0] in b_phy_n.keys():
                self.b_phy[b_phy_n[self.a[0]]]=self.a[1]
            elif self.a[0] in DM_n.keys():
                self.DM[DM_n[self.a[0]]]=self.a[1]
            elif self.a[0]==6:
                self.gm2=self.a[1]
        return
    
    def readNMHMIX(self):
        if 'Hmix' not in self.__dict__.keys():
            self.Hmix={}
        self.Hmix['S']={}
        while self.InBlock():
            if type(self.a[1]) is int:
                self.Hmix['S'][tuple(self.a[:2])]=self.a[2]
        return
    
    def readNMAMIX(self):
        if 'Hmix' not in self.__dict__.keys():
            self.Hmix={}
        self.Hmix['P']={}
        while self.InBlock():
            if type(self.a[1]) is int:
                self.Hmix['P'][tuple(self.a[:2])]=self.a[2]
        return
    
    def readNMNMIX(self):
        self.Nmix={}
        while self.InBlock():
            if type(self.a[1]) is int:
                self.Nmix[tuple(self.a[:2])]=self.a[2]


    def readREDCOUP(self):
        self.Hcouplings={}
        while self.InBlock():
            if type(self.a[1]) is int:
                self.Hcouplings[tuple(self.a[:2])]=self.a[2]
        return

    def readFINETUNING(self):
        self.FINETUNING={}
        while self.InBlock():
            if type(self.a[0]) is int:
                self.FINETUNING[self.a[0]]=self.a[1]
        self.FT=self.FINETUNING[sorted(self.FINETUNING.keys())[-2]]
        return
    
    def readLHCCROSSSECTIONS(self):
        self.LHCCROSSSECTIONS={}
        while self.InBlock():
            if type(self.a[0]) is int:
                self.LHCCROSSSECTIONS[self.a[0]]=self.a[1]
        return

    def readLHCFIT(self):
        self.LHCfit={}
        LHCfit_n={1:'hrr',2:'hff',3:'hVV'}
        while self.InBlock():
            if self.a[0] in LHCfit_n.keys():
                self.LHCfit[LHCfit_n[self.a[0]]]=self.a[1]
        return

    def readHiggsBoundsResults(self):
        while self.InBlock():
            if self.a[0]==1:
                if self.a[1]==2:
                    self.HBresult=self.a[2]
        return
    
    def readHiggsSignalsResults(self):
        while self.InBlock():
            if self.a[0]==13:
                self.HSresult=self.a[1]
        return
    
    def readNDMCROSSSECT(self):
        if 'DM' not in self.__dict__.keys():
            self.DM={}
        while self.InBlock():
            if self.a[-1]:
                self.DM[['CS','csPsi','csNsi','csPsd','csNsd'][self.a[0]]]=self.a[1]
        return
    
    def readABUNDANCE(self):
        self.DMAnnihilation={}
        while self.InBlock():
            if self.a[0]==7:
                self.DMAnnihilation[tuple(self.a[2:6])]=self.a[6]
        return
    
    def readANNIHILATION(self):
        while self.InBlock():
            if self.a[0]==0:
                self.sigmaV=self.a[1]
        return

    def readDCINFO(self):
        self.DecayList={}
        id=0
        while self.InBlock():
            if type(self.a[0]) is str:
                if self.a[0].upper()=='DECAY':
                    id=self.a[1]
                    self.DecayList[id]={'width':self.a[2]}
            elif (type(self.a[0]) is float) and (len(self.a)>=4):
                if self.a[1]==2:
                    self.DecayList[id][tuple(self.a[2:4])]=self.a[0]
                elif self.a[1]==3:
                    self.DecayList[id][tuple(self.a[2:5])]=self.a[0]



class readSLHA(readBLOCK):
    def __init__(self,discountKeys=[]):
        self.discount=discountKeys

    def read(self,file):

        f=open(file,'r')
        self.lines=f.readlines()
        f.close()

        omegafile=file.replace('spectr','omega')
        if os.path.isfile(omegafile):
            f=open(omegafile,'r')
            self.lines+=f.readlines()
            f.close()
    
        self.p=True
        self.i=0
        try:
            while self.p:
                a=readline(self.lines[self.i])
                self.i+=1
                if type(a[0]) is str:
                    if a[0].upper()=='BLOCK':
                        if hasattr(readBLOCK,'read'+a[1]):
                            getattr(readBLOCK,'read'+a[1])(self)
        except IndexError:# End of the file
            if hasattr(self,'DecayList'):
                self.Decay=translate(self.DecayList)