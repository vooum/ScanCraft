#!/usr/bin/env python3

import sys,os,shutil

print(sys.argv)
if len(sys.argv)<2: exit('key of directory name should be given')

key=sys.argv[1]
if len(sys.argv)==3:
    OutSteam=sys.argv[2]
else:
    OutSteam='out'
if not os.path.exists(OutSteam): os.mkdir(OutSteam)
#------ check directory ./out
for files in os.listdir(OutSteam):
    if 'mcmc' in files:
        exit('mcmc files in '+OutSteam)
#------ get all mcmc files
number=0
for files in os.listdir():
    if key in files and os.path.isdir(files):
        for directory in os.listdir(files):
            if 'mcmc' in directory:
                number+=1
                inname=os.path.join(files,directory)
                outname=os.path.join(OutSteam,'mcmc'+str(number))
                while os.path.exists(outname):
                    number+=1
                    outname=os.path.join(OutSteam,'mcmc'+str(number))
                shutil.copytree(inname,outname)
print(number,' files copied')
