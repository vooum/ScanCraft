#!/usr/bin/env python3

import sys,numpy,pandas,os,queue
from copy import deepcopy
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')
from command.nexus.SPheno import SPheno,block_mapping,ReadSLHAFile
from command.scan.scan import scan
from command.multi_thread.MT_SPheno import MT_SPheno
from command.multi_thread.queue_operation import GenerateQueue # generate random queue
from command.pytorch.normalize import normalize
from command.operators.iterable import FlatToList
from command.data_transformer.ArrayToInputQueue import ArrayToInputQueue
from command.data_transformer.InputToPandas import InputToPandas
from command.data_transformer.defult_parameter_order import defult_name_order
from command.file_operations.GetSamples import GetSamples

from command.scan.GA import ga


# a mold of input point object
mold=scan(method='random')
# MinPar -------
mold.AddScalar('tanB','MINPAR',3,1.,60.)
# Extpar -------
# mold.AddScalar('A_Lambda','EXTPAR' ,63,-3.e3,3.e3)
# mold.AddScalar('A_kappa','EXTPAR',64, -5.e2, 5.e2)
# mold.AddScalar('mu_eff', 'EXTPAR',65,100., 300.)
# NMSSMRUNIN ------
mold.AddScalar('Lambda','NMSSMRUN', 1, 1e-3, 0.7, prior_distribution='exponential')
mold.AddScalar('Kappa', 'NMSSMRUN', 2, 1e-3, 0.7, prior_distribution='exponential')
mold.AddScalar('T_Lambda','NMSSMRUN',3,2   , 1.4E3)
mold.AddScalar('T_Kappa ','NMSSMRUN',4,-3.5E2,3.5E2)
mold.AddScalar('Vs','NMSSMRUN',     5, 200.,7E5)
# MSoft --------
# mold.AddScalar('M1','MSOFT',1,50,2000)
# mold.AddScalar('M2','MSOFT',2,100,2000)
# Squark -------
# mold.AddElement( 'Mq3^2','MSQ2',(3,3), 1e4,4e6)
# mold.AddElement( 'Mu3^2','MSU2',(3,3), 1e4,4e6)
# mold.AddFollower('Md3^2','MSD2',(3,3), 'Mu32')
mold.AddElement( 'Tt',   'TU',  (3,3), -2000,2000)
mold.AddElement( 'Tb',   'TD',  (3,3), -2000,2000)
# Slepton ------
mold.AddElement( 'Ml3^2','MSL2',(3,3), 1e4,25e4)
mold.AddElement( 'Ml2^2','MSL2',(2,2), 1e4,25e4)
# mold.AddFollower('Ml1^2','MSL2',(1,1),'Ml32')
# mold.AddFollower('Me3^2','MSE2',(3,3),'Ml32')
# mold.AddFollower('Me2^2','MSE2',(2,2),'Ml32')
# mold.AddFollower('Me1^2','MSE2',(1,1),'Ml32')
mold.AddElement( 'Ttau', 'TE',  (3,3),-2000,2000)
# Sneutrino ----
mold.AddElement( 'Mv3^2', 'MV2', (3,3), 1e4, 9e4)
mold.AddElement( 'Mv2^2', 'MV2', (2,2), 1e4,25e4)
mold.AddElement( 'Mx3^2', 'MX2', (3,3), 1e4, 9e4)
mold.AddElement( 'Mx2^2', 'MX2', (2,2), 1e4,25e4)
mold.AddElement( 'Yv3',   'YV',  (3,3), 0, 0.5)
mold.AddElement( 'Tv3',   'TV',  (3,3), -500,500)
mold.AddElement( 'Yv2',   'YV',  (2,2), 0,0.5)
mold.AddElement( 'Tv2',   'TV',  (2,2), -500,500)
mold.AddElement( 'Lambda_v3',  'LAMN', (3,3), 0,  0.5)
mold.AddElement( 'Lambda_v2',  'LAMN', (2,2), 0,  0.5)
mold.AddElement( 'T_Lambda_v3','TLAMN',(3,3), -500,500)
mold.AddElement( 'T_Lambda_v2','TLAMN',(2,2), -500,500)
# muX
for i in range(1,4):
    for j in range(1,4):
        mold.AddDependent(f'muX_{i}{j}','MUX',tuple((i,j)))
# function to get each muX elements
from command.ISS_mu_x import GetMuX as muX
def GetMuX(sample):
    #input: Yv_11, Yv_22, Yv_33, LAMN_11, LAMN_22, LAMN_33, tanbeta, vs
    M=muX(0.01,# Yv_11
        sample.variable_list['Yv2'](),
        sample.variable_list['Yv3'](),
        0.3,# LAMN_11
        sample.variable_list['Lambda_v2'](),
        sample.variable_list['Lambda_v3'](),
        sample.variable_list['Lambda_v2'](),
        sample.variable_list['tanB'](),
        sample.variable_list['tanB']()/sample.variable_list['Lambda']()
    )
    for i in range(1,4):
        for j in range(1,4):
            sample.variable_list[f'muX_{i}{j}'].value=M[i-1,j-1]

order=defult_name_order(mold.free_parameter_list) # parameter name list
dimention=len(order)

Norm=normalize(mold,order=order) # set operation scale=(a,b) to scale parameters to (a,b) range

# Set multi-thread SPheno ==========
MTS=MT_SPheno(threads=7,Renew=False#'NInvSeesaw'
            ,input_mold='LesHouches.in.NInvSeesaw_low'
            ,input_file='LesHouches.in.NInvSeesaw_low'
            ,output_file='SPheno.spc.NInvSeesaw'
            ,main_routine='SPhenoNInvSeesaw')
    # threads: number of threads of multi-thread-SPheno, number larger than CPU-thread is worthless.
    # if bool(Renew) is True, old copies of SPheno packages will be replaced by new copies.
ReMake=None
    # If None, default value of ReMake will be same as Renew.
    # Each copy of SPheno will be 'make clean' then 'make = {ReMake}',
    # set this to False once SPheno copies are re-made
Gene=ga() # Gene Algorithm

def Chisqure(sample):
    X2_h=(sample.MASS[35]-125.01)**2/9
    # X1_h=(sample.MASS[25]-95)**2/25
    return X2_h+X1_h

accepted_list=[[]]# list of calculable input points
sample_list=[[]]  # list of spectrum of points in accepted_list
input_array_list=[]
X2s_list=[]

generation=0
# +++++ 0_generation: Random or read from files ++++++
if False:#True:# Read 0_generation from files ===============
    path='./output/record_180626_171635/'
    samples=GetSamples(path=path,patterns=['in','out'])
    for sample in samples:
        if len(sample.documents)==2:
            inp=deepcopy(mold)
            inp.GetValue(sample.documents['in'],mapping=block_mapping)
            accepted_list[0].append(inp)
            sample.Merge(SPheno.Read(None,sample.documents['out']))
            sample_list[0].append(sample)
else:   # Random 0_generation ============
    while len(accepted_list[generation])<100:
        sample_queue=GenerateQueue(mold,lenth=100)
        for i in range(100):
            point=sample_queue.get()
            GetMuX(point)
            sample_queue.put(point)
        MTS.Run(sample_queue,report_interval=100,ReMake=ReMake)
        ReMake=False
        accepted_list[0].extend(MTS.accepted_list)
        sample_list[0].extend(MTS.sample_list)
exit()
# ++++++++

# record 0_generation into lists
input_array=InputToPandas(accepted_list[generation],order=order,title=f'generation_{generation}')
X2s=numpy.array(list(map(Chisqure,sample_list[generation]))).reshape(-1,1)
input_array_list.append(input_array)
X2s_list.append(X2s)

for generation in range(1,51):
    storage=numpy.hstack([ Norm(input_array), X2s ])
    Gene.Generation_new(storage[:100])
    accepted_list.append([])
    sample_list.append([])
    storage=numpy.array([])
    while len(accepted_list[generation])<100:
        input_new=Norm.D(Gene.Generation_Next())
        ArrayToInputQueue(input_new,mold,order=order,q=sample_queue)
        MTS.Run(sample_queue,report_interval=100)
        accepted_list[generation].extend(MTS.accepted_list)
        sample_list[generation].extend(MTS.sample_list)
    input_array=InputToPandas(accepted_list[generation],order=order,title=f'generation_{generation}')
    X2s=numpy.array(list(map(Chisqure,sample_list[generation]))).reshape(-1,1)
    X2s_list.append(X2s)
