#! /usr/bin/env python3
import sys
sys.path.append('/home/vooum/Desktop/ScanCommando')

from command.data_type import *
from command.SPheno import SPheno
from command.scan import scan

mcmc=scan()
mcmc.Add('tanB','MINPAR',3,1,40)
mcmc.AddMatrix('lambda_N','LAMNIN',shape=(3,3),free_element=((3,3),),pace='normal')


# print(mcmc.variable_list['try'].block)
# mcmc.variable_list['try'].value=3232
# print([mcmc.block_list['temp'][i].value for i in mcmc.block_list['temp'].keys()])
print(mcmc.variable_list['lambda_N'].free_element)
print(mcmc.variable_list['lambda_N'].element_list)

#print(type(mcmc.variable_list['trymtx'])is matrix)
#print(mcmc.variable_list.keys(),'\n',mcmc.block_list.keys())


S=SPheno(main_routine='./bin/SPhenoNInvSeesaw',in_model='LesHouches.in.NInvSeesaw_low.ES1')
mcmc.variable_list['tanB'].value=15.8
mcmc.variable_list['lambda_N'].element_list[(3,3)]=0.07
#print(mcmc.variable_list['lambda_N'].element_list)

S.run(mcmc)
