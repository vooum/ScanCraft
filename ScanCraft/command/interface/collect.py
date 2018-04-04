#!/usr/bin/env python3

import sys,argparse,os#,pandas,numpy
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')


parser=argparse.ArgumentParser(
    prog='collect',add_help=False,
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

#argv=parser.parse_args()