#!/usr/bin/env python3
import os,shutil,subprocess
__all__=['run','NMSSMToolsDir','inpModelDir','inpDir','spectrDir','omegaDir',
         'recordDir','recordchisq','recordpar','recordlist']

DataDir='mcmc/'
if not os.path.isdir(DataDir): os.mkdir(DataDir)

_CurDir=os.getcwd()
print(_CurDir)
NMSSMToolsDir=''
for i in os.listdir(_CurDir):
    if 'NMSSMTools' in i and os.path.isdir(i):
        NMSSMToolsDir=max(NMSSMToolsDir,i)
else:
    if NMSSMToolsDir=='': exit('no NMSSMTools package found')
    else: NMSSMToolsDir=os.path.join(_CurDir,NMSSMToolsDir)
inpModelDir = os.path.join(DataDir,'inp.dat')
inpDir = os.path.join(DataDir,'mcmcinp.dat')
spectrDir=os.path.join(DataDir,'mcmcspectr.dat')
omegaDir=os.path.join(DataDir,'mcmcomega.dat')
recordDir=os.path.join(DataDir,'record/')
run='./run '+os.path.join('../',inpDir)
recordchisq=open(os.path.join(DataDir,'chisqure'),'w')
recordpar=open(os.path.join(DataDir,'recordpar'),'w')
recordlist=open(os.path.join(DataDir,'recordlist'),'w')
if os.path.exists(recordDir):
    if input('clean record? y/n \n')=='n':
        exit('Directory record/ is not deleted')
    else:
        shutil.rmtree(recordDir)
os.mkdir(recordDir)

if not os.path.exists(os.path.join(NMSSMToolsDir,'main/nmhdecay')):
    subprocess.Popen('make init', cwd=NMSSMToolsDir, shell=True).wait()
    subprocess.Popen('make', cwd=NMSSMToolsDir, shell=True).wait()
else: print(os.path.join(NMSSMToolsDir,'main/nmhdecay'),'exist')
