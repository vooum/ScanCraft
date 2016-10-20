#!/usr/bin/env python3
from command import *
from command.operator.getpoint import GetPoint
import subprocess,random,math,shutil
#print([ i for i in globals().keys() if '__' not in i])


# settings
ism='M_h2'
target=1000
StepFactor=1. # sigma = n% of (maximum - minimum) of the free parameters
SlopFactor=.3 # difficulty of accepting a new point with higher chisq
add_chisq=True
ignore=[ 'Landau Pole'#27
        ,'Relic density'#30
        ,'b->s gamma'#32
        ,'B_s->mu+mu-'#35
        ,'Muon magn'#37
        ,'No Higgs in the'#46
        ,'b -> c tau nu'#58 always keep alive
        ]
r=readSLHA(discountKeys=ignore)

#print(read.readline.readline)
#print(mcmc.Scan)

free=mcmc.Scan()
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
print('Start point is:')
GetPoint(free,'inp.dat')

free.SetRandom()


L_Nsd=DarkMatter('LUX2016_Nsd.txt')
L_Psd=DarkMatter('LUX2016_Psd.txt')
L_Psi=DarkMatter('LUX201608_Psi.txt')

record=-1
trypoint=0
lastchisq=1e10
# scan ==================================================================
while record < target:

    if trypoint%100==1: print(trypoint,' points tried; ',record,' points recorded')
    trypoint+=1

    N.run(free)

    r.read(N.spectrDir)
    '''
    print(sorted(r.Decay.__dict__))
    print(list(r.__dict__.keys()))
    print(r.Decay.St_1)
    exit()'''

    if r.p:
        mainNNo=0
        mixV=0
        for i in range(5):
            if abs(r.Nmix[tuple([1,i+1])]) > abs(mixV):
                mixV=r.Nmix[tuple([1,i+1])]
                mainNNo=i+1
        
        #if mainNNo not in [3,4,5]:continue
        if False:#'csNsd' in r.DM.keys():
            if abs(r.DM['csNsd'])>L_Nsd.value(r.Msp['X_N1']):continue
            if abs(r.DM['csPsd'])>L_Psd.value(r.Msp['X_N1']):continue
            if abs(r.DM['csPsi'])>L_Psi.value(r.Msp['X_N1']):continue
        chisq=0.
        chisq_Q={}
        chisq_A={}
        # chisqure
        chisq_Q['mh']=chi2(r.Mh[ism],mh)
        chisq_Q['bsg']=chi2(r.b_phy['b_sg']*1e4,bsg)
        chisq_Q['bmu']=chi2(r.b_phy['b_mu']*1e9,bmu)
        chisq_Q['DM']=chi2(r.DM['DMRD'],omg)
        #chisq_A['FT']=(max(r.FT,40.)-40.)**2/100.
        for i in chisq_Q.values():
            chisq+=i
        if add_chisq :
            for i in chisq_A.values(): 
                chisq+=i
        #   record point
        if (random.random() < math.exp(max(SlopFactor*min(lastchisq-chisq,0.),-745))
    	    or chisq<10.):
            lastchisq=chisq
            free.record()
            print(record,'points recorded.')
            print('\nnew point accepted: -------------------')
            print('x2=  ',chisq,'\nx2_i= ',chisq_Q,chisq_A)
            print('Higgs masses: ',r.Mh)
            free.print()

            record+=1
            shutil.copyfile(N.inpDir,os.path.join(N.recordDir,'inp.'+str(record)))
            shutil.move(N.spectrDir,os.path.join(N.recordDir,'spectr.'+str(record)))
            shutil.move(N.omegaDir,os.path.join(N.recordDir,'omega.'+str(record)))

    free.GetNewPoint(StepFactor)
    