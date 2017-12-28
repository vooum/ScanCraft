#!/usr/bin/env python3

import sys,argparse
sys.path.append('/home/heyangle/Desktop/ScanCraft/ScanCraft')

from command.interface.collect import parser as collect_parser

parser=argparse.ArgumentParser(parents=[collect_parser])
parser.add_argument('--version',action='version',version='%(prog)s 0.02',help='version')
argv=parser.parse_args()
# print(argv)