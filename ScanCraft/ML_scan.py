#!/usr/bin/env python3

import sys,pandas,numpy
import torch
from torch import nn
from torch.nn import functional
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')
from command.scan.scan import scan
from command.pytorch.normalize import GetRanges
from command.pytorch.classify import Classify,BCEloss
from command.pytorch.estimate import Estimate,MSELoss
from command.pytorch.normalize import normalize#,NormalizeArray,DenormalizeArray
from command.pytorch.variable import CudaVariableFromArray, ArrayFromCudaVariable

mold=scan(method='random')
mold.AddScalar('tanB','MINPAR',3,1.,60.)
# mold.AddScalar('M1','EXTPAR',1  ,20.    ,1000.)
# mold.AddScalar('M2','EXTPAR'   ,2  ,100.    ,2000.)
mold.AddScalar('Atop','EXTPAR'   ,11  ,  -6e3    ,6e3)
mold.AddFollower('Abottom','EXTPAR'   ,12,'Atop')
# mold.AddScalar('Atau','EXTPAR'   ,13  ,  100.      ,2000.)
# mold.AddFollower('MtauL','EXTPAR'   ,33,'Atau')
# mold.AddFollower('MtauR','EXTPAR'   ,36,'Atau')
# mold.AddScalar('MQ3L','EXTPAR'   ,43,	100.,	2.e3)
# mold.AddScalar('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3)
# mold.AddFollower('MbottomR','EXTPAR'  ,49,'MtopR')
mold.AddScalar('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,prior_distribution='exponential')
mold.AddScalar('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,prior_distribution='exponential')
mold.AddScalar('A_Lambda','EXTPAR' ,63,-3.e3,3.e3)
mold.AddScalar('A_kappa','EXTPAR' ,64,-3.e3,3.e3)
mold.AddScalar('mu_eff','EXTPAR'  ,65,100.,1500.)

data_range=GetRanges(mold.free_parameter_list)
print('Input mode been set')

IsCalculable=Classify(7,1000,500).cuda()
c_opt=torch.optim.Adam(IsCalculable.parameters(),lr=0.01)
EstimateMh=Estimate(7,500,300).cuda()
e_opt=torch.optim.Adam(EstimateMh.parameters(),lr=0.001)
print('NNs been set')

# '''arrays of original training samples and test samples'''
acc_train =pandas.read_csv('laboratory/Pylon/accepted_train.csv',header=[0,1,2,3],index_col=0)
exc_train =pandas.read_csv('laboratory/Pylon/excluded_train.csv',header=[0,1,2,3],index_col=0)
mh_train  =pandas.read_csv('laboratory/Pylon/mass_train.csv',    header=[0,1,],   index_col=0)


Norm=normalize(mold)
# calculable
c_data_train  =numpy.vstack((acc_train.values,exc_train.values[:13718]))
c_inp_train   =Norm(c_data_train[:,:7])
c_target_train=c_data_train[:,-1].reshape((len(c_data_train),1))
in_CV=CudaVariableFromArray(c_inp_train)
target_CV=CudaVariableFromArray(c_target_train,requires_grad=False)

# acc_test  =pandas.read_csv('laboratory/Pylon/accepted_test.csv' ,header=[0,1,2,3],index_col=0)
# exc_test  =pandas.read_csv('laboratory/Pylon/excluded_test.csv' ,header=[0,1,2,3],index_col=0)
# mh_test   =pandas.read_csv('laboratory/Pylon/mass_test.csv'     ,header=[0,1,],   index_col=0)
# c_data_test   =numpy.vstack((acc_test.values,exc_test.values[:6632]))
# c_inp_test    =Norm(c_data_test[:,:7])
# c_target_test =c_data_test[:,-1].reshape((len(c_data_test),1))

# estimate Higgs mass
in_EV    =CudaVariableFromArray(Norm(acc_train.values[:,:-1]))
target_EV=CudaVariableFromArray(numpy.log10(mh_train.values))

print('Training with raw data:')

# # calculable
# for i in range(1000):
#     pred=IsCalculable(in_CV)
#     loss=BCEloss(pred,target_CV)
#     if i%100==0:
#         print(i,loss.data[0])
#     c_opt.zero_grad()
#     loss.backward()
#     c_opt.step()
# print(loss)
# # higgs mass
# for i in range(1000):
#     pred=EstimateMh(in_EV)
#     loss=MSELoss(pred,target_EV)
#     if i%100==0:
#         print(i,loss.data[0])
#     e_opt.zero_grad()
#     loss.backward()
#     e_opt.step()
# print(loss)

# print('generate new points:')

