#!/usr/bin/env python3

class outputfile:
    def __init__(self,filename):
        self.file=open(filename,'w')
    def number(self,N):
        self.file.write(N+'\t')
    def Data(self,ParList):
        for d in ParList:
            self.file.write('\t'.join([(str(ii)+': '+str(d[ii])) for ii in sorted(d)])+'\t')
        self.file.write('\n')
        


