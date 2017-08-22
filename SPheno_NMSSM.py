#! /usr/bin/env python3
import sys,copy,random,math
sys.path.append('/home/vooum/Desktop/ScanCommando')

from command.data_type import *
from command.SPheno import SPheno
from command.MicrOMEGAs import MicrOMEGAs
from command.scan import scan
from command.chisqure import *
from command.outputfile import *

import subprocess



ism='all'
target_number=1000
step_factor=1. # sigma = n% of (maximum - minimum) of the free parameters
slop_factor=1. # difficulty of accepting a new point with higher chisq

Data=DataFile(Dir='mcmc')


mcmc=scan()
mcmc.Add('tanB',    'MINPAR',3,1,40)
mcmc.Add('Lambda',  'EXTPAR',61,1e-5,1.,pace='normal')
mcmc.Add('Kappa',   'EXTPAR',62,1e-5,1.,pace='normal')
mcmc.Add('MuEff',   'EXTPAR',65,1e2,1.5e3)
mcmc.Add('T_Lambda','NMSSMRUNIN',3,-2e3,2e3,pace='normal')
mcmc.Add('T_Kappa', 'NMSSMRUNIN',4,-1e3,1e3,pace='normal')

mcmc.AddMatrix('T_e','TEIN',shape=(3,3),free_element={(3,3):None},minimum=-5000,maximum=5000)
mcmc.AddMatrix('T_u','TUIN',shape=(3,3),free_element={(3,3):None},minimum=-5000,maximum=5000)
mcmc.AddMatrix('T_d','TDIN',shape=(3,3),free_element={(3,3):None},minimum=-5000,maximum=5000)

#mcmc.AddMatrix('lambda_N','LAMNIN',shape=(3,3),free_element={(3,3):None},minimum=0.,maximum=0.5)

mcmc.GetValue('./mcmc/SPheno.in')

newpoint=copy.deepcopy(mcmc) #=mcmc.GetNewPoint()

S=SPheno(main_routine='./bin/SPhenoNMSSM',in_model='SPheno.in',output_file='SPheno.spc.NMSSM')
#M=MicrOMEGAs()
HB=HiggsBounds(S.package_dir,mode='SARAH')
HS=HiggsSignals(S.package_dir,mode='SARAH')


#spectr=S.Run(newpoint)
#print(spectr.MINPAR[3])
record_number=-1
try_point=0
last_chisq=1e50
while record_number < target_number:
    try_point+=1
    if try_point%1000==1:
        print('Trying point %i; %i points recorded; current X2 is %.3e'%(try_point,record_number,last_chisq))
    if try_point>1e10:break

    #-- run SPheno
    spectr=S.Run(newpoint)
    if not spectr:
        #print('No output')
        newpoint=mcmc.GetNewPoint(step_factor)
        continue

    #-- run HiggsBounds and HiggsSignals
    hb=HB.RunSARAH()
    # if hb.HBresult==0.:
    #     newpoint=mcmc.GetNewPoint(step_factor)
    #     continue
    hs=HS.RunSARAH()

    chisq_list={}
    chisq_list['h_sm']=min(chi2(spectr.MASS[25],mh),chi2(spectr.MASS[35],mh))
    chisq_list['bsg']=chi2(spectr.FLAVORKITQFV[200]*1e4,bsg)
    chisq_list['bmu']=chi2(spectr.FLAVORKITQFV[4006]*1e9,bmu)

    chisq_list['HB']=(max(hb.obsratio,1)-1.)*10.
    chisq_list['HS']=abs(math.log(hs.Pvalue))

    chisq=sum(chisq_list.values())
    if (random.random() < math.exp(max(slop_factor * min( last_chisq-chisq,0.),-745))
    	or chisq<10.):
        last_chisq=chisq
        mcmc=newpoint
        print(record_number,'points recorded.\n')
        print('\nnew point accepted: -------------------')
        print('x2=  ',chisq,'\nx2_i= ',chisq_list)
        print('Higgs masses: ',[spectr.MASS.get(i) for i in [25,35,45] ] )
        print('\nParameters:')
        newpoint.Print()
        
        record_number+=1
        S.Record(record_number)
        #exit()
        
        Data.In('AllParameters.txt').record(spectr.MINPAR,spectr.EXTPAR,spectr.NMSSMRUN)
        Data.In('Mass.txt').record(spectr.MASS)
        Data.In('Chisqure.txt').record({'Total':chisq},chisq_list)
    newpoint=mcmc.GetNewPoint(step_factor)


'''
    #-- run MicrOMEGAs
    omega=M.Run(S.output_dir)
    #-- Dwarf Spheroidal Galaxies of Fermi-LAT
    subprocess.Popen('./')
    
'''