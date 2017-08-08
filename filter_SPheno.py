#! /usr/bin/env python3
import sys,os,re,copy,shutil
sys.path.append('/home/vooum/Desktop/ScanCommando')
from command.Experiments.directdetection import DirectDetection
from command.read.readSLHA import ReadFiles
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

L_Nsd=DirectDetection('PandaX_Nsd_2016.txt')
L_Psd=DirectDetection('PandaX_Psd_2016.txt')
L_Psi=DirectDetection('LUX201608_Psi.txt')

outNumber=-1

for dirs in spectrs.keys():
    for files in spectrs[dirs]:
        spectr=ReadFiles(files)