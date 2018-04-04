#! /usr/bin/env python3
import sys,copy
sys.path.append('/home/heyangle/Desktop/ScanCommando/ScanCommando')

from command.data_type import *
from command.SPheno import SPheno
from command.MicrOMEGAs import MicrOMEGAs
from command.scan import scan

import subprocess



ism='all'
target_number=1000
step_factor=1. # sigma = n% of (maximum - minimum) of the free parameters
slop_factor=1. # difficulty of accepting a new point with higher chisq






mcmc=scan()
mcmc.Add('tanB','MINPAR',3,1,40)
mcmc.AddMatrix('lambda_N','LAMNIN',shape=(3,3),free_element={(3,3):None},minimum=0.,maximum=0.5)

mcmc.GetValue('./mcmc/SPheno.spc.NInvSeesaw')

newpoint=copy.deepcopy(mcmc) #=mcmc.GetNewPoint()

S=SPheno(main_routine='./bin/SPhenoNInvSeesaw',in_model='LesHouches.in.NInvSeesaw_low.ES1')
M=MicrOMEGAs()


#spectr=S.Run(newpoint)
#print(spectr.MINPAR[3])
record_number=-1
try_point=0
last_chisq=1e10
while record_number < target_number:
    if try_point%100==1:
        print('%i points tried; %i points recorded; current X2 is %.3e'%(try_point,record_number,last_chisq))
    try_point+=1
    if try_point>1e3:break

    chisq=0
    chisq_list={}
    #-- run SPheno
    spectr=S.Run(newpoint)
    #-- run MicrOMEGAs
    omega=M.Run(S.output_dir)
    #-- Dwarf Spheroidal Galaxies of Fermi-LAT
    subprocess.Popen('./')
    
