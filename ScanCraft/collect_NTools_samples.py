#!/usr/bin/env python3
import sys,argparse,os#,pandas,numpy
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')
from command.file_operations.GetDirectories import GetDirectories
from command.file_operations.GetSamples import GetSamples


parser=argparse.ArgumentParser(
    prog='collect',
    description='collect data files of samples from multiple folders'
    )
# folder_info group
folder_info=parser.add_argument_group(
    title='folder info',
    description='infomation to search folders'
)
folder_info.add_argument(
    '--path','-p',
    default='./',#metavar='location',
    help='relative path to find folders'
    )
folder_info.add_argument(
    '--keyword','-k',
    default='mcmc',metavar='pattern',
    help='folders that we want must have names containing this keyword'
)
folder_info.add_argument(
    '--numbered',action='store_true',
    help='whether folder names must contain a number'
)
folder_info.add_argument(
    '--subfolder','-s',
    default='record',#metavar='name',
    help='name of subfolder that contain data files in each folder')
# file_info group
file_info=parser.add_argument_group(
    title='data file info',
    description='information to collect data files'
)
file_info.add_argument(
    '--name','-n',nargs='*',
    default=['inp','spectr','omega'],#metavar='name',
    help='name of data files will contain one of these strings'
    )
# target
parser.add_argument(
    '--copy','-c',
    type=str,
    help='copy all data files to the specified folder'
)

argv=parser.parse_args()

# print(argv.__dict__)

folders=GetDirectories(path=argv.path,keyword=argv.keyword,numbered=argv.numbered)
sample_collect=[
    GetSamples( path=os.path.join( folder,argv.subfolder ), patterns=argv.name )
    for folder in folders
]
samples=sum(sample_collect,[])

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