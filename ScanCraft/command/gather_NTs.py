#!/usr/bin/env python3

import sys,os,pandas,numpy
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')
from pandas.core.frame import DataFrame

from command.NMSSMTools import ReadNMSSMToolsSpectr
from command.operations.GetFiles import GetFiles
from command.format.block_table import block_table
# from command.

ignore=[ 'Landau Pole'
        ,'relic density'
        ,'Muon magn. mom.'
        ,'b -> c tau nu'
        ,'direct detection'
        ,'b -> c tau nu'#58 always keep alive
        ]

if len(sys.argv)>3:
    exit('too much argv(argument value)s')

try:
    similarity=sys.argv[1].rstrip('/')
except IndexError:
    similarity='mcmc'
#     OutSteam='Analysed'
# else:
#     try:
#         OutSteam=sys.argv[2].rstrip('/')
#     except:
#         OutSteam='Analysed'

# os.mkdir(OutSteam)
# AnalysedDir=os.path.join(OutSteam,'record')
# os.mkdir(AnalysedDir)
# Data=DataFile(Dir=OutSteam)

directory_list=GetFiles('./',similarity=similarity,HasNumber=False)
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

Data=DataFrame({})
for ith,document in enumerate(input_list):
    if ith%100==0:
        print('recording %ith, total %i'%(ith,total))

    spectr=ReadNMSSMToolsSpectr(document,ignore=ignore)
    # inNumber=re.findall(r'\d+',document)[-1]
    # outNumber+=1   # reNumber

    col_name=['No_','path']
    value_row=[ith,document]

    for block,code_value_dict in spectr.__dict__.items():
        # print(block_name)
        try:
            code_2_name=getattr(block_table,block)
        except AttributeError:
            continue
        else:
            for code,value in code_value_dict.items():
                try:
                    col_name.append(code_2_name(code))
                except KeyError:
                    raise# continue
                else:
                    value_row.append(value)
    Data=Data.append(
        DataFrame(numpy.array([value_row]),columns=col_name),
        ignore_index=True)

Data.to_csv('Data_%s.csv'%similarity)