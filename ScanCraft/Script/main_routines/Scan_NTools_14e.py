#!/usr/bin/env python3
import sys,os,re,copy,shutil,subprocess,random,math
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')

from command.scan import scan
from command.NMSSMTools import NMSSMTools
from command.operations.getpoint import GetPoint
from command.Experiments.directdetection import DirectDetection
from command.chisqure import *
mh=[125.09, 3., 3.]
from command.data_type import *
# from command.MicrOMEGAs import MicrOMEGAs
from command.outputfile import *
#print([ i for i in globals().keys() if '__' not in i])


# settings
ism='all'
target_number=1000
step_factor=1.1 # sigma = n% of (maximum - minimum) of the free parameters
slop_factor=1. # difficulty of accepting a new point with higher chisq
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
#free.Add('tanB','MINPAR',3,1.,60.)
free.Add('M1','EXTPAR',1  ,20.    ,4000.)
free.Add('M2'	,'EXTPAR'   ,2  ,100.    ,4000.)
#free.Add('Atop'	,'EXTPAR'   ,11  ,  -6e3    ,6e3)
#free.Add('Abottom','EXTPAR'   ,12,-6e3,6e3,pace='follow Atop')
free.Add('Atau'	,'EXTPAR'   ,13  ,  100.      ,1.e4)
free.Add('MtauL','EXTPAR'   ,33,	100.,	1.e4,pace='follow Atau')
free.Add('MtauR','EXTPAR'   ,36,	100.,	1.e4,pace='follow Atau')
#free.Add('MQ3L'	,'EXTPAR'   ,43,	100.,	2.e3)
#free.Add('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3)
#free.Add('MbottomR','EXTPAR'  ,49,	100.,	2.e3 ,pace='follow MtopR')
#free.Add('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,pace='lognormal')
#free.Add('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,pace='lognormal')
free.Add('A_Lambda','EXTPAR' ,63,-3.e3,3.e3)
free.Add('A_Kappa','EXTPAR' ,64,-3.e3,3.e3)
#free.Add('mu_eff','EXTPAR'  ,65,100.,1500.)
#free.Add('MA','EXTPAR',124,	0.,	2.e3)

N=NMSSMTools()
free.GetValue('./mcmc/inp.dat')
print('Start point is:')
newpoint=copy.deepcopy(free)
newpoint.Print()

Data=DataFile(Dir='mcmc')

record_number=-1
try_point=0
last_chisq=1e10
# scan ==================================================================
while record_number < target_number:
    try_point+=1
    if try_point%1000==1:
        print('Trying point %i; %i points recorded; current X2 is %.3e'%(try_point,record_number,last_chisq))
    if try_point>1e10:break

    spectr=N.Run(newpoint,ignore=ignore)

    if spectr.ERROR:
        newpoint=free.GetNewPoint(step_factor)
        print(spectr.SPINFO)
        continue
    
    chisq_list={}

    chisq_list['constraints']=len(spectr.constraints)*1e3
    chi_h1=chi2(spectr.MASS[25],mh)
    chi_h2=chi2(spectr.MASS[35],mh)
    if 'h1' in ism.lower():
        chisq_list['h_sm']=chi_h1
    elif 'h2' in ism.lower():
        chisq_list['h_sm']=chi_h2
    # else:     
    #     chisq_list['h_sm']=min(chi_h1,chi_h2)
    chisq_list['bsg']=chi2(spectr.LOWEN[1]*1e4,bsg)
    chisq_list['bmu']=chi2(spectr.LOWEN[4]*1e9,bmu)
    chisq_list['LHCfit']=sum(spectr.LHCFIT.values())

    omg=spectr.ABUNDANCE[4]
    eps=omg/0.1197
    chisq_list['DMRD']=X2(OMG=omg)

    chisq_list['mDM_14']=max(1400-spectr.LSP[0],0)**2/1E4

    chisq=sum(chisq_list.values())

    #   record point
    if (random.random() < math.exp(max(slop_factor * min( last_chisq-chisq,0.),-745))
        or chisq<10.
        ):
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

        Data.In('Chisqure.txt').record({'Total':chisq},chisq_list)

        for file_name in [
            'MINPAR','EXTPAR','NMSSMRUN','MSOFT','HMIX','MASS',
            'YD','YE','YU','TD','TE','TU','MSQ2','MSL2','MSD2','MSU2','MSE2',
            'NDMCROSSSECT','ABUNDANCE','ANNIHILATION'
            ]:
            if hasattr(spectr,file_name):
                Data.In(file_name).record(getattr(spectr,file_name))
    else:
        print(chisq,chisq_list,'discarded')
    newpoint=free.GetNewPoint(step_factor)

    