#!/usr/bin/env python3
import sys,os,re,copy,shutil,subprocess,random,math
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')

from command.scan.scan import scan
from command.NMSSMTools import NMSSMTools
from command.Experiments.directdetection import DirectDetection
from command.chisqure import *
mh=[125.09, 3., 3.]
from command.format.parameter_type import *
from command.MicrOMEGAs import MicrOMEGAs
from command.outputfile import *
#print([ i for i in globals().keys() if '__' not in i])


# settings
ism='all'
target_number=10
step_factor=10. # sigma = n% of (maximum - minimum) of the free parameters
slop_factor=1. # difficulty of accepting a new point with higher chisq
ignore=[ 'Landau Pole'#27
        ,'relic density'#30
        ,'b->s gamma'#32
        ,'B_s->mu+mu-'#35
        ,'Muon magn'#37
        ,'No Higgs in the'#46
        ,'b -> c tau nu'#58 always keep alive
        ]

# setup parameter point
free=scan()
# Lambda,Kappa,A_Lambda,A_Kappa,mu,tanBeta,A_t
free.AddScalar('tanB','MINPAR',3,1.,60.)

# setup NMSSMTools controller
N=NMSSMTools(input_mold='./mcmc/inp.dat')

# get values from NMSSMTools input file
free.GetValue('./mcmc/inp.dat')
print('Start point is:')
newpoint=copy.deepcopy(free)
newpoint.Print()

# set directory to save data
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
        newpoint=copy.deepcopy(free).Sample(step_factor=step_factor)
        print(spectr.SPINFO)
        continue
    
    chisq_list={}

    chisq_list['constraints']=len(spectr.constraints)*1e4
    chi_h1=chi2(spectr.MASS[25],mh)
    chi_h2=chi2(spectr.MASS[35],mh)
    if 'h1' in ism.lower():
        chisq_list['h_sm']=chi_h1
    elif 'h2' in ism.lower():
        chisq_list['h_sm']=chi_h2
    else:     
        chisq_list['h_sm']=min(chi_h1,chi_h2)
    chisq_list['bsg']=chi2(spectr.LOWEN[1]*1e4,bsg)
    chisq_list['bmu']=chi2(spectr.LOWEN[4]*1e9,bmu)
    chisq_list['LHCfit']=sum(spectr.LHCFIT.values())
    chisq=sum(chisq_list.values())

    #   record point
    if (random.random() < math.exp(max(slop_factor * min( last_chisq-chisq,0.),-745))
        # or chisq<10.
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
    newpoint=copy.deepcopy(free).Sample(step_factor=step_factor)

    