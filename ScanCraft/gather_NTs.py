#!/usr/bin/env python3

import sys,os,pandas
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')

from command.NMSSMTools import ReadNMSSMToolsSpectr
from command.operations.GetFiles import GetFiles

# from command.

if len(sys.argv)>3:
    exit('too much argv(argument value)s')

try:
    similarity=sys.argv[1].rstrip('/')
    try:
        OutSteam=sys.argv[2].rstrip('/')
    except:
        OutSteam='Analysed'
except:
    similarity='mcmc'    
os.mkdir(OutSteam)
AnalysedDir=os.path.join(OutSteam,'record')
os.mkdir(AnalysedDir)
Data=DataFile(Dir=OutSteam)

directory_list=GetFiles('./',similarity=similarity)
input_list=[]
print(
'getting documents from:'   #------------------
)
for directory in directory_list:
    print('   ',directory)
    if os.path.isdir( os.path.join(directory,'record') ):
        input_list_i=GetFiles(os.path.join(directory,'record'),similarity='spectr')
    else:
        input_list_i=GetFiles(directory,similarity='spectr')
    input_list.extend(input_list_i)
total=len(input_list)
print(total,' found:\n',input_list[:5],'...')
