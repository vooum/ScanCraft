#!/usr/bin/env python3
#from command import *
from command.mcmc import Scan
from command.NMSSMTools import NMSSMTools
from command.operations.getpoint import GetPoint
from command.Experiments.directdetection import DirectDetection
from command.chisqure import *
import subprocess,random,math,shutil
#print([ i for i in globals().keys() if '__' not in i])


# settings
ism='M_h2'
target=1000
StepFactor=.1 # sigma = n% of (maximum - minimum) of the free parameters
SlopFactor=.3 # difficulty of accepting a new point with higher chisq
ignore=[ 'Landau Pole'#27
        ,'relic density'#30
        ,'b->s gamma'#32
        ,'B_s->mu+mu-'#35
        ,'Muon magn'#37
        ,'No Higgs in the'#46
        ,'b -> c tau nu'#58 always keep alive
        ]
#r=readSLHA(discountKeys=ignore)

#print(read.readline.readline)
#print(mcmc.Scan)

free=Scan()
#free.add(name,block,PDG,min,max,walk='flat',step=None,value=None)
free.add('tanB','MINPAR',3,2.,60.,step=None)
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
GetPoint(free,'./mcmc/inp.dat')
print('Start point is:')
for name in free.VariableList:
    parameter=getattr(free,name)
    print(parameter.name,parameter.PDG,parameter.value)
free.SetRandom()


L_Nsd=DirectDetection('PandaX_Nsd_2016.txt')
L_Psd=DirectDetection('PandaX_Psd_2016.txt')
L_Psi=DirectDetection('LUX201608_Psi.txt')

rec_list=open('./mcmc/record_list','w')
rec_X2=open('./mcmc/record_chisq','w')
rec_full=open('./mcmc/record_full','w')


record=-1
trypoint=0
lastchisq=1e10
# scan ==================================================================
while record < target:

    if trypoint%100==1: print(trypoint,' points tried; ',record,' points recorded')
    trypoint+=1

    r=N.run(free,ignore=ignore)
    #print(r.PROB,r.p)

    if r.p:
        mainNNo=0
        mixV=0
        #for i in range(5):
        #    if abs(r.Nmix[tuple([1,i+1])]) > abs(mixV):
        #        mixV=r.Nmix[tuple([1,i+1])]
        #        mainNNo=i+1
        
        #if mainNNo not in [3,4,5]:continue
        #print(r.DM)

        chisq=0.
        chisq_Q={}
        # chisqure
        chisq_Q['PROB']=len(r.PROB)*1e4

        if ism.upper()=='ALL':  # X2_mh
            chisq_Q['mh']=min(chi2(r.Mh['M_h1'],mh),chi2(r.Mh['M_h2'],mh))
        else:
            chisq_Q['mh']=chi2(r.Mh[ism],mh)

        chisq_Q['bsg']=chi2(r.b_phy['b_sg']*1e4,bsg)
        chisq_Q['bmu']=chi2(r.b_phy['b_mu']*1e9,bmu)

        if 'DMRD' in r.DM.keys():
            eps=r.DM['DMRD']/0.1197
            chisq_Q['DMRD']=X2(OMG=r.DM['DMRD'])#chi2(r.DM['DMRD'],omg)
            if 'csNsd' in r.DM.keys():
                #if abs(r.DM['csNsd'])*eps>L_Nsd.value(r.Msp['X_N1']):continue
                #if abs(r.DM['csPsd'])*eps>L_Psd.value(r.Msp['X_N1']):continue
                #if abs(r.DM['csPsi'])*eps>L_Psi.value(r.Msp['X_N1']):continue
                for key,DDexp in {'csNsd':L_Nsd,'csPsd':L_Psd,'csPsi':L_Psi}.items():
                    cs=abs(r.DM[key])*eps
                    limit=DDexp.value(r.Msp['X_N1'])
                    if cs>limit:
                        chisq_Q[key]=((cs-limit)/limit)**2
        else:
            chisq_Q['DMRD']=1e4
        #chisq_Q['FT']=(max(r.FT,40.)-40.)**2/100.
        for i in chisq_Q.values():
            chisq+=i
        #   record point
        if (random.random() < math.exp(max(SlopFactor*min(lastchisq-chisq,0.),-745))
    	    or chisq<10.):
            lastchisq=chisq
            free.record()
            print(record,'points recorded.')
            print('\nnew point accepted: -------------------')
            print('x2=  ',chisq,'\nx2_i= ',chisq_Q)
            print('Higgs masses: ',r.Mh)
            free.print()

            record+=1
            N.record(record)

            rec_X2.write(str(record)+'\tchisq: '+str(chisq)+'\t'+repr(chisq_Q)+'\n')
            rec_X2.flush()
    free.GetNewPoint(StepFactor)
    