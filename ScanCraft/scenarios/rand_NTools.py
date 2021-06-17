#!/usr/bin/env python3

import sys,pandas
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')
from command.scan.scan import scan
from command.NMSSMTools import NMSSMTools
from command.multi_thread.queue_operation import GenerateQueue#,FillQueue
from command.multi_thread.MT_NTools import MT_NTools
from command.data_transformer.InputListToPandas import InputListToPandas as I2P

mold=scan(method='random')
mold.AddScalar('tanB','MINPAR',3,1.,60.)
mold.AddScalar('M1','EXTPAR',1  ,20.    ,1000.)
mold.AddScalar('M2','EXTPAR'   ,2  ,100.    ,2000.)
mold.AddScalar('Atop','EXTPAR'   ,11  ,  -6e3    ,6e3)
mold.AddFollower('Abottom','EXTPAR'   ,12,'Atop')
mold.AddScalar('Atau','EXTPAR'   ,13  ,  100.      ,2000.)
mold.AddFollower('MtauL','EXTPAR'   ,33,'Atau')
mold.AddFollower('MtauR','EXTPAR'   ,36,'Atau')
mold.AddScalar('MQ3L','EXTPAR'   ,43,	100.,	2.e3)
mold.AddScalar('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3)
mold.AddFollower('MbottomR','EXTPAR'  ,49,'MtopR')
mold.AddScalar('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,prior_distribution='exponential')
mold.AddScalar('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,prior_distribution='exponential')
mold.AddScalar('A_Lambda','EXTPAR' ,63,-3.e3,3.e3)
mold.AddScalar('A_kappa','EXTPAR' ,64,-3.e3,3.e3)
mold.AddScalar('mu_eff','EXTPAR'  ,65,100.,1500.)

MTN=MT_NTools(threads=6)
ore_q=GenerateQueue(mold,lenth=10)
MTN.Run(ore_q)

if len(MTN.accepted_list)>0:
    acc=I2P(MTN.accepted_list,title='accepted')
    # acc[('accepted','points','are','calculable')]=1
    acc[('flags','binary','1/0_is/not','calculable')]=1
    acc.to_csv('accepted.csv')
if len(MTN.excluded_list)>0:
    exc=I2P(MTN.excluded_list,title='excluded')
    # exc[('excluded','points','mass','negative')]=0
    exc[('flags','binary','1/0_is/not','calculable')]=0
    exc.to_csv('excluded.csv')