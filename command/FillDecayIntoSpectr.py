#!/usr/bin/env python3

import sys,os

if len(sys.argv)<2:
    exit('in put filename')

for files in os.listdir(sys.argv[1]):
    name=os.path.join(sys.argv[1],files)
    if 'decay' in files and os.path.isfile(name):
        os.system('cat '+name+' >> '+name.replace('decay','spectr'))