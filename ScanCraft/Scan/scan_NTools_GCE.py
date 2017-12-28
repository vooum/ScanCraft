#!/usr/bin/env python3
import sys,copy,random,math,subprocess,shutil

from command.data_type import *
from command.NMSSMTools import NMSSMTools
from command.MicrOMEGAs import MicrOMEGAs
from command.scan import scan
from command.chisqure import *
from command.outputfile import *

#from command.operations.getpoint import GetPoint
from command.Experiments.directdetection import DirectDetection
#from GCE.GCE import chisq_GCE as GCE
#print([ i for i in globals().keys() if '__' not in i])


# settings
ism='all'
target_number=1000
step_factor=.2 # sigma = n% of (maximum - minimum) of the free parameters
slop_factor=.3 # difficulty of accepting a new point with higher chisq
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

free=scan()
#free.add(name,block,PDG,min,max,walk='flat',step=None,value=None)
free.Add('tanB','MINPAR',3,2.,60.)
free.Add('M1','EXTPAR',1  ,20.    ,1000.)
free.Add('M2'	,'EXTPAR'   ,2  ,100.    ,2000.)
free.Add('Atop'	,'EXTPAR'   ,11  ,  -6e3    ,6e3)
free.Add('Abottom','EXTPAR'   ,12,-6e3,6e3,pace='follow Atop')
free.Add('Atau'	,'EXTPAR'   ,13  ,  100.      ,2000.)
free.Add('MtauL','EXTPAR'   ,33,	100.,	2.e3,pace='follow Atau')
free.Add('MtauR','EXTPAR'   ,36,	100.,	2.e3,pace='follow Atau')
free.Add('MQ3L'	,'EXTPAR'   ,43,	100.,	2.e3)
free.Add('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3)
free.Add('MbottomR','EXTPAR'  ,49,	100.,	2.e3 ,pace='follow MtopR')
free.Add('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,pace='lognormal')
free.Add('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,pace='lognormal')
free.Add('A_kappa','EXTPAR' ,64,-3.e3,3.e3)
free.Add('mu_eff','EXTPAR'  ,65,100.,1500.)
free.Add('MA','EXTPAR',124,	0.,	2.e3)

#print(free.block_list);exit()

L_Nsd=DirectDetection('PandaX_Nsd_2016.txt')
L_Psd=DirectDetection('PandaX_Psd_2016.txt')
L_Psi=DirectDetection('LUX201608_Psi.txt')

rec_list=open('./mcmc/record_list','w')
rec_X2=open('./mcmc/record_chisq','w')
rec_full=open('./mcmc/record_full','w')

Data=DataFile(Dir='mcmc')

N=NMSSMTools(in_model='inpZ3.dat')
free.GetValue('inp.dat')
print('Start point is:')
for name,par in free.variable_list.items():
    print(name,par.block,par.PDG,par.value)

newpoint=copy.deepcopy(free)

record_number=-1
try_point=0
last_chisq=1e50
# scan ==================================================================
while record_number < target_number:
    try_point+=1
    if try_point%1000==1:
        print('Trying point %i; %i points recorded; current X2 is %.3e'%(try_point,record_number,last_chisq))
    if try_point>1e10:break

    spectr=N.Run(newpoint,ignore=ignore)
    if spectr.ERROR:
        newpoint=free.GetNewPoint(step_factor)
        continue
    
    chisq_list={}

    chisq_list['constraints']=len(spectr.constraints)*1e4
    chisq_list['h_sm']=min(chi2(spectr.MASS[25],mh),chi2(spectr.MASS[35],mh))
    chisq_list['bsg']=chi2(spectr.LOWEN[1]*1e4,bsg)
    chisq_list['bmu']=chi2(spectr.LOWEN[4]*1e9,bmu)

    if hasattr(spectr,'ABUNDANCE'):
        omg=spectr.ABUNDANCE[4]
        eps=omg/0.1197
        chisq_list['DMRD']=X2(OMG=omg)#chi2(r.DM['DMRD'],omg)
    else:
        chisq_list['DMRD']=1e4
    if hasattr(spectr,'NDMCROSSSECT'):
        for name,ID,DDexp in [ ['csPsi',1,L_Psi],['csPsd',3,L_Psd],['csNsd',4,L_Nsd] ]:
            cs=abs(spectr.NDMCROSSSECT[ID])*eps
            limit=DDexp.value(spectr.LSP[0])
            if cs>limit:
                chisq_list[name]=((cs-limit)/limit)**2/10.

    
    #         chisq_Q['GCE']=(max(GCE(N.spectrDir)-20.,0))**2
    #         print(chisq_Q['GCE'])#;exit()
    
    chisq=sum(chisq_list.values())
    if (random.random() < math.exp(max(slop_factor * min( last_chisq-chisq,0.),-745))
    	or chisq<10.):
        last_chisq=chisq
        free=newpoint
        print(record_number,'points recorded.\n')
        print('\nnew point accepted: -------------------')
        print('x2=  ',chisq,'\nx2_i= ',chisq_list)
        print('Higgs masses:\n\t',[spectr.MASS.get(i) for i in [25,35,45] ] )
        print('constraints:\n\t'+'\n\t'.join(spectr.constraints))
        print('\nParameters:')
        newpoint.Print()

        record_number+=1
        N.Record(record_number)

        Data.In('AllParameters.txt').record(spectr.MINPAR,spectr.EXTPAR,spectr.NMSSMRUN)
        Data.In('Mass.txt').record(spectr.MASS)
        Data.In('Chisqure.txt').record({'Total':chisq},chisq_list)
    newpoint=free.GetNewPoint(step_factor)