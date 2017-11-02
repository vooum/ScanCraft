#!/usr/bin/env python3
import sys,os,re,copy,shutil
sys.path.append('/home/heyangle/Desktop/ScanCommando/ScanCommando')

from command.read.readSLHA import *
from command.NMSSMTools import ReadNMSSMToolsSpectr
from command.Experiments.directdetection import *
from command.outputfile import *
from command.operations.GetFiles import GetFiles

print(sys.argv)

ignore=[ 'Landau Pole'
        ,'relic density'
        ,'Muon magn. mom.'
        ,'b -> c tau nu'
        ,'direct detection'
        ,'b -> c tau nu'#58 always keep alive
        ]

if len(sys.argv)==1:
    similarity='mcmc'
else:
    similarity=sys.argv[1].rstrip('/')
if len(sys.argv)==3:
    OutSteam=sys.argv[2].rstrip('/')
elif len(sys.argv)>3:
    exit('too much argv(argument value)s')
else:
    OutSteam='Analysed'
if os.path.exists(OutSteam):exit('Directory '+ OutSteam +' already exist')
os.mkdir(OutSteam)
AnalysedDir=os.path.join(OutSteam,'record')
os.mkdir(AnalysedDir)
Data=DataFile(Dir=OutSteam)

# output files ===================================

#-------------- get all spectr and omega files
# spectrs={}
# record='record'
# for dirs in os.listdir():
#     spectri=[]
#     if key in dirs and os.path.isdir(dirs):
#         for files in os.listdir(os.path.join(dirs,record)):
#             #if files=='spectr.0':continue
#             name=os.path.join(os.getcwd(),dirs,record,files)
#             if 'spectr' in files and os.path.isfile(name) and 'from' not in files:
#                 spectri.append(name)
#         spectri.sort(key=lambda x: int(re.findall(r'\d+',x)[-1]))
#         spectrs[dirs]=spectri
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

# L_Nsd=DirectDetection('PandaX_Nsd_2016.txt')
# L_Psd=DirectDetection('PandaX_Psd_2016.txt')
# L_Psi=DirectDetection('LUX201608_Psi.txt')

outNumber=-1
for ith,document in enumerate(input_list):
    if ith%100==1:
        print('%i recorded, runing %ith, total %i'%(outNumber,ith+1,total))

    spectr=ReadNMSSMToolsSpectr(document,ignore=ignore)
    if spectr.ERROR:print(spectr.SPINFO);continue
    if spectr.constraints:print(spectr.SPINFO);continue
    inNumber=re.findall(r'\d+',document)[-1]
    outNumber+=1   # reNumber
    #outNumber=int(inNumber) #keep original Number
    omega=ReadSLHAFile(document.replace('spectr.dat','Omega.txt'))

    for file_name in [
        'MINPAR','EXTPAR','NMSSMRUN','MSOFT','HMIX','MASS',
        # 'YD','YE','YU','TD','TE','TU','MSQ2','MSL2','MSD2','MSU2','MSE2',
        'NDMCROSSSECT','ABUNDANCE','ANNIHILATION'
        ]:
        if hasattr(spectr,file_name):
            Data.In(file_name).record(getattr(spectr,file_name))

    for file_name in [
        'NDMCROSSSECT','ABUNDANCE','INDIRECT_CHISQUARES','ANNIHILATION'
        ]:
        if hasattr(omega,file_name):
            Data.In(file_name+'_O').record(getattr(omega,file_name))

    continue
    # copy files
    outspectr=os.path.join(AnalysedDir,'spectr.'+str(outNumber))
    shutil.copyfile(files,outspectr)
    shutil.copyfile(files.replace('spectr','inp'),outspectr.replace('spectr','inp'))
    shutil.copyfile(files.replace('spectr','omega'),outspectr.replace('spectr','omega'))
