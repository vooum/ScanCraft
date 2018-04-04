#!/usr/bin/env python3
import sys,argparse,os,pandas,numpy,copy
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')
from command.file_operations.GetDirectories import GetDirectories
from command.file_operations.GetSamples import GetSamples

from command.interface.collect import parser as collect_parser

parser=argparse.ArgumentParser(parents=[collect_parser])
parser.add_argument('--version',action='version',version='%(prog)s 0.02',help='version')
argv=parser.parse_args()

# print(argv.__dict__)

folders=GetDirectories(path=argv.path,keyword=argv.keyword.rstrip('/'),numbered=argv.numbered)
sample_collect=[
    GetSamples( path=os.path.join( folder,argv.subfolder ), patterns=argv.name )
    for folder in folders
]
samples=sum(sample_collect,[])

# copy all data files to argv.copy
if argv.copy:
    number=-1
    os.mkdir(argv.copy)
    os.mkdir(os.path.join(argv.copy,'record'))
    for sample in samples:
        number+=1
        new_documents={}
        new_documents['inp']=os.path.join(argv.copy,'record','inp.dat.'+str(number))
        new_documents['spectr']=new_documents['inp'].replace('inp','spectr')
        new_documents['omega']=new_documents['inp'].replace('inp','omega')
        sample.MoveTo(new_documents)

# output data table
from command.scan import scan
from command.NMSSMTools import NMSSMTools
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


for sample in samples:
    sample.input=copy.deepcopy(mold)
    in_file=sample.documents['inp']
    sample.input.GetValue(in_file)
    number=int(os.path.basename(in_file).split('.')[-1])
    print(number)

input_list=[point.input for point in samples]
input_table=I2P(input_list,title='accepted')
input_table[('flags','binary','1/0_is/not','calculable')]=1

input_table.to_csv(os.path.join('accepted.csv'))