#!/usr/bin/env python3
import subprocess,random,math,shutil,sys,re,os
import numpy as np
sys.path.append('/home/heyangle/Desktop/programing/ScanCommando/')

from command import *
from command.operations.getpoint import GetPoint
from command.read.readSLHA import readSLHA
from command import mcmc
from command.NMSSMTools import NMSSMTools
from command.Experiments.directdetection import DirectDetection
from command.chisqure import *
from command.outputfile import *
#print([ i for i in globals().keys() if '__' not in i])


# settings
ism='M_h2'
StepFactor=.2 # sigma = n% of (maximum - minimum) of the free parameters
SlopFactor=1. # difficulty of accepting a new point with higher chisq
add_chisq=True
ignore=['Landau Pole'#27
        ,'relic density'#30
        ,'DM direct detection rate'
        ,'b->s gamma'#32
        ,'B_s->mu+mu-'#35
        ,'Muon magn'#37
        ,'No Higgs in the'#46
        ,'b -> c tau nu'#58 always keep alive
       ]
r = readSLHA(discountKeys=ignore)

#print(read.readline.readline)
#print(mcmc.Scan)

free=mcmc.Scan()
#free.add(name,block,PDG,min,max,walk='flat',step=None,value=None)
free.add('tanB','MINPAR',3,1.,60.,step=None)
free.add('M1','EXTPAR',1  ,20.    ,1000.,step=None)
free.add('M2'	,'EXTPAR'   ,2  ,100.    ,2000.,step=None)
free.add('Atop'	,'EXTPAR'   ,11  ,  -6e3    ,6e3,step=None)
free.add('Abottom','EXTPAR'   ,12,-6e3,6e3,walk=free.Atop)
free.add('Atau'	,'EXTPAR'   ,13  ,  100.      ,2000.,step=None)
free.add('MtauL','EXTPAR'   ,33,	100.,	2.e3,walk=free.Atau)
free.add('MtauR','EXTPAR'   ,36,	100.,	2.e3,walk=free.Atau)
free.add('MQ3L'	,'EXTPAR'   ,43,	100.,	2.e3,step=None)
free.add('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3,step=None)
free.add('MbottomR','EXTPAR'  ,49,	100.,	2.e3 ,walk=free.MtopR)
free.add('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,walk='log',step=None)
free.add('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,walk='log',step=None)
free.add('A_kappa','EXTPAR' ,64,-3.e3,3.e3,step=None)
free.add('mu_eff','EXTPAR'  ,65,100.,1500.,step=None)
free.add('MA','EXTPAR',124,	0.,	2.e3)

N=NMSSMTools()
print('Start point is:')
#GetPoint(free,'inp.dat')

#free.SetRandom()


L_Nsd=DirectDetection('PandaX_Nsd_2016.txt')
L_Psd=DirectDetection('PandaX_Psd_2016.txt')
L_Psi=DirectDetection('LUX201608_Psi.txt')

record=-1
trypoint=0
lastchisq=1e10


#get all points
spectrs=[]
for files in os.listdir(sys.argv[1]):
    name=os.path.join(sys.argv[1],files)
    if 'inp.' in files and os.path.isfile(name) and 'from' not in files:
        spectrs.append(name)
spectrs.sort(key=lambda x: int(re.findall(r'\d+',x)[-1]))
#print(spectrs);exit()
survived=open('survived.txt','w')


# scan ==================================================================
#while record < target:
for point in spectrs:
    GetPoint(free,point)
    #free.print()
    #if trypoint%100==1: print(trypoint,' points tried; ',record,' points recorded')
    trypoint+=1

    N.run(free,attr='value')

    r.read(N.spectrDir)


    if r.p:
        if len(r.PROB)!=0:print(point,r.PROB);continue
        chisq=0.
        chisq_Q={}
        chisq_A={}
        if 'DMRD' in r.DM.keys():
            eps=r.DM['DMRD']/0.1197
            chisq_Q['DMRD']=X2(OMG=r.DM['DMRD'])#chi2(r.DM['DMRD'],omg)
            if 'csNsd' in r.DM.keys():
                for key,DDexp in {'csNsd':L_Nsd,'csPsd':L_Psd,'csPsi':L_Psi}.items():
                    cs=abs(r.DM[key])*eps
                    limit=DDexp.value(r.Msp['X_N1'])
                    if cs>limit:
                        chisq_Q[key]=((cs-limit)/limit)**2
        else:
            continue
        if 'csNsd' in chisq_Q.keys(): continue
        if 'csPsd' in chisq_Q.keys(): continue
        if 'csPsi' in chisq_Q.keys(): continue
        

        # chisqure
        chisq_Q['PROB']=len(r.PROB)*1e5
        chisq_Q['mh']=chi2(r.Mh[ism],mh)
        chisq_Q['bsg']=chi2(r.b_phy['b_sg']*1e4,bsg)
        chisq_Q['bmu']=chi2(r.b_phy['b_mu']*1e9,bmu)

        for i in chisq_Q.values():
            chisq+=i
        if add_chisq :
            for i in chisq_A.values(): 
                chisq+=i
        #   record point
        if True:# or (random.random() < math.exp(max(SlopFactor*min(lastchisq-chisq,0.),-745))
    	    #or chisq<10.):
            record=re.findall(r'\d+',point)[-1]
            print(record,'point recorded.')
            print('\nnew point accepted: -------------------')
            print('x2=  ',chisq,'\nx2_i= ',chisq_Q,chisq_A)
            print('Higgs masses: ',r.Mh)
            free.print()

            Data.In('BlockMass').record(r.Mass)
            Data.In('Ft.txt').record(r.FT,r.FINETUNING[sorted(r.FINETUNING.keys())[-1]])

            N.record(record)

    