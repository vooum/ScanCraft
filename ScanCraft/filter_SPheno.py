#! /usr/bin/env python3
import sys,os,re,copy,shutil
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')
from command.Experiments.directdetection import DirectDetection
from command.read.readSLHA import ReadFiles
from command.Experiments.colliders import LHC
from command.outputfile import *

print(sys.argv)

if len(sys.argv)==1:
    key='mcmc'
else:
    key=sys.argv[1].rstrip(' /')
if len(sys.argv)==3:
    OutSteam=sys.argv[2]
elif len(sys.argv)>3:
    exit('too much argv(argument value)s')
else:
    OutSteam='Analysed'
if os.path.exists(OutSteam):exit('Directory '+ OutSteam +' already exist')
os.mkdir(OutSteam)
AnalysedDir=os.path.join(OutSteam,'record')
os.mkdir(AnalysedDir)
Data=DataFile(Dir=OutSteam)

spectrs={}
record='record'
for dirs in os.listdir():
    spectri=[]
    if key in dirs and os.path.isdir(dirs):
        for files in os.listdir(os.path.join(dirs,record)):
            #if files=='spectr.0':continue
            name=os.path.join(os.getcwd(),dirs,record,files)
            if 'SPheno.spc.' in files and os.path.isfile(name) and 'from' not in files:
                spectri.append(name)
        spectri.sort(key=lambda x: int(re.findall(r'\d+',x)[-1]))
        spectrs[dirs]=spectri

# L_Nsd=DirectDetection('PandaX_Nsd_2016.txt')
# L_Psd=DirectDetection('PandaX_Psd_2016.txt')
# L_Psi=DirectDetection('LUX201608_Psi.txt')

outNumber=-1

for dirs in spectrs.keys():
    for files in spectrs[dirs]:
        spectr=ReadFiles(files)

        ism=None
        for hi in [25,35]:
            mh=spectr.MASS[hi]
            if mh>121 and mh<129:
                ism=hi
                break
        else:
            if ism==None:
                continue
            else:
                exit('wrong')

        mh=spectr.MASS[25]
        bsg=spectr.FLAVORKITQFV[200]
        if bsg<min(LHC.bsg) or bsg>max(LHC.bsg):continue
        bmu=spectr.FLAVORKITQFV[4006]
        if bmu<min(LHC.bmu) or bmu>max(LHC.bmu):continue

        outNumber+=1
        #Data.In('AllParameters.txt').record(spectr.MINPAR,spectr.EXTPAR,spectr.NMSSMRUN)
        for file_name in [
            'MINPAR','EXTPAR','NMSSMRUN','MSOFT','HMIX','MASS','NMNMIX'
            'YD','YE','YU','TD','TE','TU','MSQ2','MSL2','MSD2','MSU2','MSE2']:
            Data.In(file_name).record(getattr(spectr,file_name))
        
        # continue
        out_spectr=os.path.join(AnalysedDir,'SPheno.spc.NMSSM.'+str(outNumber))
        shutil.copyfile(files,out_spectr)
        shutil.copyfile(files.replace('spc.NMSSM','in'),out_spectr.replace('spc.NMSSM','in'))
