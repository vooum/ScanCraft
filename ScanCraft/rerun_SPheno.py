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

mcmc=scan()
mcmc.Add('tanB',    'MINPAR',3,1,40)
mcmc.Add('Lambda',  'EXTPAR',61,1e-5,1.,pace='normal')
mcmc.Add('Kappa',   'EXTPAR',62,1e-5,1.,pace='normal')
mcmc.Add('MuEff',   'EXTPAR',65,1e2,1.5e3)
mcmc.Add('T_Lambda','NMSSMRUNIN',3,-2e3,2e3,pace='normal')
mcmc.Add('T_Kappa', 'NMSSMRUNIN',4,-1e3,1e3,pace='normal')

mcmc.AddMatrix('T_e','TEIN',shape=(3,3),free_element={(3,3):None},minimum=-5000,maximum=5000)
mcmc.AddMatrix('T_u','TUIN',shape=(3,3),free_element={(3,3):None},minimum=-5000,maximum=5000)
mcmc.AddMatrix('T_d','TDIN',shape=(3,3),free_element={(3,3):None},minimum=-5000,maximum=5000)

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

S=SPheno(main_routine='./bin/SPhenoNMSSM',in_model='SPheno.in',output_file='SPheno.spc.NMSSM')
HB=HiggsBounds(S.package_dir,mode='SARAH')
HS=HiggsSignals(S.package_dir,mode='SARAH')
# MOmega=MicrOMEGAs(data_dir=OutSteam)

outNumber=-1
for ith,document in enumerate(input_list):
    mcmc.GetValue(document)
    spectr=S.Run(mcmc)

    if not spectr:print(spectr.SPINFO);continue
    hb=HB.RunSARAH()
    hs=HS.RunSARAH()

    inNumber=re.findall(r'\d+',document)[-1]
    outNumber+=1   # reNumber
    #outNumber=int(inNumber) #keep original Number

    for file_name in [
        'MINPAR','EXTPAR','NMSSMRUN','MSOFT','HMIX','MASS','NMNMIX',
        'YD','YE','YU','TD','TE','TU','MSQ2','MSL2','MSD2','MSU2','MSE2',
        'NDMCROSSSECT','ABUNDANCE','ANNIHILATION'
        ]:
        if hasattr(spectr,file_name):
            Data.In(file_name).record(getattr(spectr,file_name),Number=outNumber)
    Data.In('record_list').record(document,Number=outNumber)


    S.Record(outNumber)
    shutil.copy(hb.output_dir,os.path.join(S.record_dir,'HiggsBounds_results.dat'+str(outNumber)))
    shutil.copy(hs.output_dir,os.path.join(S.record_dir,'HiggsSignals_results.dat'+str(outNumber)))

    print('%i recorded, runing %ith, total %i'%(outNumber,ith+1,total))