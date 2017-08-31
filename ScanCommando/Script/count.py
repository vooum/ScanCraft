#!/usr/bin/env python3
import os,sys

key=sys.argv[1]
dirs=[]
for i in os.listdir('./'):
  if key in i:
    dirs.append(os.path.join(i,'mcmc/record/'))

print(dirs)
N=0
for i in dirs:
  if os.path.exists(i):
    N+=len(os.listdir(i))
print(N)
