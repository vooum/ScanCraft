#!/usr/bin/env python3
import sys,os,re,copy,shutil
sys.path.append('/home/heyangle/Desktop/ScanCommando/ScanCommando')

from command.read.readSLHA import *
from command.NMSSMTools import *
from command.Experiments.directdetection import *
from command.outputfile import *
from command.scan import scan
from command.operations.GetFiles import GetFiles
from command.MicrOMEGAs import MicrOMEGAs


print(sys.argv)

ignore=[ 'Landau Pole'
        ,'relic density'
        ,'Muon magn. mom.'
        ,'b -> c tau nu'
        ,'direct detection'
        ,'b -> c tau nu'#58 always keep alive
        ]

free=scan()
#free.add(name,block,PDG,min,max,walk='flat',step=None,value=None)
free.Add('tanB','MINPAR',3,2.,60.)
free.Add('M1','EXTPAR',1  ,20.    ,1000.)
free.Add('M2'	,'EXTPAR'   ,2  ,100.    ,2000.)
free.Add('Atop'	,'EXTPAR'   ,11  ,  -6e3    ,6e3)
free.Add('Abottom','EXTPAR'   ,12,-6e3,6e3,pace='follow Atop')
free.Add('Atau'	,'EXTPAR'   ,13  ,  100.      ,2000.)
free.Add('MtauL','EXTPAR'   ,33,	100.,	2.e3,pace='follow Atau')
free.Add('MtauR','EXTPAR'   ,36,	100.,	2.e3,pace='follow Atau')
free.Add('MQ3L'	,'EXTPAR'   ,43,	100.,	2.e3)
free.Add('MtopR'	,'EXTPAR'   ,46,	100.,	2.e3)
free.Add('MbottomR','EXTPAR'  ,49,	100.,	2.e3 ,pace='follow MtopR')
free.Add('Lambda','EXTPAR'  ,61  ,1e-3    ,1. ,pace='lognormal')
free.Add('Kappa','EXTPAR'   ,62 ,1.e-3    ,1. ,pace='lognormal')
free.Add('A_kappa','EXTPAR' ,64,-3.e3,3.e3)
free.Add('mu_eff','EXTPAR'  ,65,100.,1500.)
free.Add('MA','EXTPAR',124,	0.,	2.e3)

if len(sys.argv)==1:
    similarity='mcmc'
else:
    similarity=sys.argv[1].rstrip('/')
if len(sys.argv)==3:
    OutSteam=sys.argv[2].rstrip('/')
elif len(sys.argv)>3:
    exit('too much argv(argument value)s')
else:
    OutSteam='ReCalculated'
#if os.path.exists(OutSteam):exit('Directory '+ OutSteam +' already exist')
AnalysedDir=os.path.join(OutSteam,'record')
try:
    os.mkdir(OutSteam)
    os.mkdir(AnalysedDir)
except:
    pass
Data=DataFile(Dir=OutSteam)

directory_list=GetFiles('./',similarity=similarity)
input_list=[]
print(
'getting documents from:'
)
for directory in directory_list:
    print('   ',directory)
    if os.path.isdir( os.path.join(directory,'record') ):
        input_list_i=GetFiles(os.path.join(directory,'record'),similarity='inp')
    else:
        input_list_i=GetFiles(directory,similarity='inp')
    input_list.extend(input_list_i)
total=len(input_list)
print(total,' found:\n',input_list[:5],'...')

# L_Nsd=DirectDetection('PandaX_Nsd_2016.txt')
# L_Psd=DirectDetection('PandaX_Psd_2016.txt')
# L_Psi=DirectDetection('LUX201608_Psi.txt')

N=NMSSMTools(data_dir=OutSteam)
MOmega=MicrOMEGAs(data_dir=OutSteam)

outNumber=-1
for ith,document in enumerate(input_list):
    free.GetValue(document)
    spectr=N.Run(free,ignore=ignore)
    if spectr.ERROR:print(spectr.SPINFO);continue
    if spectr.constraints:print(spectr.SPINFO);continue

    omega=MOmega.Run(N.output_dir)
    MOmega.IDD_X2()

    X2_GCE_old=GCE(N.output_dir)
    inNumber=re.findall(r'\d+',document)[-1]
    outNumber+=1   # reNumber
    #outNumber=int(inNumber) #keep original Number

    for file_name in [
        'MINPAR','EXTPAR','NMSSMRUN','MSOFT','HMIX','MASS',
        'YD','YE','YU','TD','TE','TU','MSQ2','MSL2','MSD2','MSU2','MSE2',
        'NDMCROSSSECT','ABUNDANCE','ANNIHILATION'
        ]:
        if hasattr(spectr,file_name):
            Data.In(file_name).record(getattr(spectr,file_name))

    for file_name in [
        'NDMCROSSSECT','ABUNDANCE','INDIRECT_CHISQUARES','ANNIHILATION'
        ]:
        if hasattr(omega,file_name):
            Data.In(file_name+'_O').record(getattr(omega,file_name))
    N.Record(outNumber)
    MOmega.Record(outNumber)


    print('%i recorded, runing %ith, total %i'%(outNumber,ith+1,total))