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
class translate:
    def __init__(self,DecayList):
        for id in DecayList.keys():
            self.width={}
            setattr(self,ParticleSpectrum[id],{})
            init=getattr(self,ParticleSpectrum[id])
            for outS, outR in DecayList[id].items():
                if type(outS) is str:
                    self.width[outS]=outR
                else:
                    name=[]
                    for i in outS:
                        if i>0:
                            name.append(ParticleSpectrum[i])
                        elif i<0:
                            name.append('-'+ParticleSpectrum[-i])
                    init['&'.join(name)]=outR
        return



class readBLOCK:
    def InBlock(self):
        if self.lines[self.i][:5] == 'BLOCK':
            return False
        else:
            self.a=readline(self.lines[self.i])
            self.i+=1
            return True

    def SPINFO(self):
        self.prob=[]
        while self.InBlock():
            if self.a[0]==4:
                self.p=False
                return
            elif self.a[0]==3:
                for Key in self.discount:
                    if Key in self.a[1]:
                        break
                else:
                    self.prob.append(self.a[1])
        if len(self.prob)>0:
            self.p=False
        return

    def MINPAR(self):
        self.MinPar={}
        MinPar_n={0:'SCALE',1:'M0',2:'M12',3:'tanb',5:'A0'}
        while self.InBlock():
            if self.a[0] in MinPar_n.keys():
                self.MinPar[MinPar_n[self.a[0]]]=self.a[1]
        return
    
    def EXTPAR(self):
        self.ExtPar={}
        ExtPar_n={1:'M1',2:'M2',3:'M3'\
                ,11:'Atop',12:'Abotton',13:'Atau'\
                ,43:'MQ3',46:'MU3',49:'MB3'\
                ,61:'lambda',62:'kappa',63:'Alambda',64:'Akappa',65:'mu_eff'\
                ,124:'MA',125:'MP'}
        while self.InBlock():
            if self.a[0] in ExtPar_n.keys():
                self.ExtPar[ExtPar_n[self.a[0]]]=self.a[1]
        return

    def MASS(self):
        self.Mass={}
        self.Mh={}
        Mh_n={25:'h1',35:'h2',45:'h3',36:'A1',46:'A2',37:'Ch'}
        self.Msp={}
        Msp_n={1000022:'N1',1000023:'N2',1000025:'N3',1000035:'N4',1000045:'N5',1000024:'C1',1000037:'C2'}
        while self.InBlock():
            self.Mass[self.a[0]]=self.a[1]
            if self.a[0] in Mh_n.keys():
                self.Mh['M_'+Mh_n[self.a[0]]]=self.a[1]
            elif self.a[0] in Msp_n.keys():
                self.Msp['X_'+Msp_n[self.a[0]]]=self.a[1]
        return
    
    def LOWEN(self):
        self.b_phy={}
        b_phy_n={1:'b_sg',4:'b_mu'}
        self.DM={}
        DM_n={10:'DMRD',20:'s_Psi'}
        while self.InBlock():
            if self.a[0] in b_phy_n.keys():
                self.b_phy[b_phy_n[self.a[0]]]=self.a[1]
            elif self.a[0] in DM_n.keys():
                self.DM[DM_n[self.a[0]]]=self.a[1]
        return
    
    def NMHMIX(self):
        if 'Hmix' not in self.__dict__.keys():
            self.Hmix={}
        self.Hmix['S']={}
        while self.InBlock():
            if type(self.a[1]) is int:
                self.Hmix['S'][tuple(self.a[:2])]=self.a[2]
        return
    
    def NMAMIX(self):
        if 'Hmix' not in self.__dict__.keys():
            self.Hmix={}
        self.Hmix['P']={}
        while self.InBlock():
            if type(self.a[1]) is int:
                self.Hmix['P'][tuple(self.a[:2])]=self.a[2]
        return
    
    def NMNMIX(self):
        self.Nmix={}
        while self.InBlock():
            if type(self.a[1]) is int:
                self.Nmix[tuple(self.a[:2])]=self.a[2]


    def REDCOUP(self):
        self.Hcouplings={}
        while self.InBlock():
            if type(self.a[1]) is int:
                self.Hcouplings[tuple(self.a[:2])]=self.a[2]
        return

    def FINETUNING(self):
        self.FT_pi={}
        while self.InBlock():
            if type(self.a[0]) is int:
                self.FT_pi[self.a[0]]=self.a[1]
        self.FT=self.FT_pi[sorted(self.FT_pi.keys())[-2]]
        return
    
    def LHCFIT(self):
        self.LHCfit={}
        LHCfit_n={1:'hrr',2:'hff',3:'hVV'}
        while self.InBlock():
            if self.a[0] in LHCfit_n.keys():
                self.LHCfit[LHCfit_n[self.a[0]]]=self.a[1]
        return

    def HiggsBoundsResults(self):
        while self.InBlock():
            if self.a[0]==1:
                if self.a[1]==2:
                    self.HBresult=self.a[2]
        return
    
    def HiggsSignalsResults(self):
        while self.InBlock():
            if self.a[0]==13:
                self.HSresult=self.a[1]
        return
    
    def NDMCROSSSECT(self):
        if 'DM' not in self.__dict__.keys():
            self.DM={}
        while self.InBlock():
            if self.a[-1]:
                self.DM[['CS','csPsi','csNsi','csPsd','csNsd'][self.a[0]]]=self.a[1]
        return

    def DCINFO(self):
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
        while self.i < len(self.lines) and self.p:
            a=readline(self.lines[self.i])
            self.i+=1
            if type(a[0]) is str:
#                if a[0].upper()=='DECAY':
#                    if hasattr(readDECAY,a[1]):
#                        readDECAY.
                if a[0].upper()=='BLOCK':
                    if hasattr(readBLOCK,a[1]):
                        getattr(readBLOCK,a[1])(self)

        self.Decay=translate(self.DecayList)
            
            
            
            
            