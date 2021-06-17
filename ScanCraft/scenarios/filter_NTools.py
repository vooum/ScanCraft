#!/usr/bin/env python3
import sys,argparse,os,re,copy,shutil
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')

from command.file_operations.GetDirectories import GetDirectories
from command.file_operations.GetSamples import GetSamples
from command.interface.collect import parser as collect_parser

from command.NMSSMTools import ReadNMSSMToolsSpectr

from command.read.readSLHA import *
from command.Experiments.directdetection import *
from command.outputfile import *

print(sys.argv)

ignore=[ 'Landau Pole'
        ,'relic density'
        ,'Muon magn. mom.'
        ,'b -> c tau nu'
        ,'direct detection'
        ,'b -> c tau nu'#58 always keep alive
        ]

# read all samples
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
for sample in samples:
    sample.spectr=ReadNMSSMToolsSpectr(sample.documents['spectr'])
    # break

# collect good samples into good_list
good_list=[]
for sample in samples:
    spectr=sample.spectr
    if (
        122<spectr.MASS[25]<128
        or spectr.ABUNDANCE[4]<0.1187*1.1
        ):
    good_list.append(sample)

# save data in dest
dest='./good_points/'
mass=open(os.path.join(dest,'MASS'),'w')
mass.write('h1\th2\n')
# and copy samples in good_list to dest_r;
dest_r=os.path.join(dest,'record/')

for number,sample in enumerate(samples):
    spectr=sample.spectr
    # save
    mass.write(f'{number}\t{spectr.MASS[25]}\t{spectr.MASS[35]}\n')
    # copy
    destinations = {
                'input'     :os.path.join(dest,'inp.dat.' + str(number)),
                'spectrum'  :os.path.join(dest,'spectr.dat.' + str(number)),
                'omega'     :os.path.join(dest,'omega.dat.' + str(number))
            }
    sample.CopyTo(destinations)