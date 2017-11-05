#!/usr/bin/env python3
import os

def sorted_keys(key_list):
    try:
        return sorted(key_list)
    except TypeError:
        dict_by_type={}
        for k in set([type(i) for i in key_list]):
            dict_by_type[k]=[]
        for i in key_list:
            dict_by_type[type(i)].append(i)

        try:
            out=sorted(dict_by_type.pop(type('1')))
        except KeyError:
            out=[]

        for i in dict_by_type.values():
            out.extend(sorted(i))
        return out
        




# class outputfile:
#     def __init__(self,filename):
#         self.file=open(filename,'w')
#     def number(self,N):
#         self.file.write(N+'\t')
#     def Data(self,ParList):
#         for d in ParList:
#             self.file.write('\t'.join([(str(ii)+': '+str(d[ii])) for ii in sorted(d)])+'\t')
#         self.file.write('\n')

class OpenDataFile():
    def __init__(self,file):
        self.file=open(file,'w')
        self.Number=-1
    def record(self,*Datalists,Number=None):
        self.Number+=1
        if type(Number) is int:
            self.file.write(str(Number))
        elif type(Number) is str:
            self.file.write(Number)
        elif Number==None:
            self.file.write(str(self.Number))
        else:
            exit(repr(Number)+' is not integer or string')

        for d in Datalists:
            self.file.write('\t')
            if type(d) is dict:
                self.file.write('\t'.join([(str(ii)+': '+str(d[ii])) for ii in sorted_keys(d.keys()) ]))
            elif type(d) is str:
                self.file.write(d)
            else:
                self.file.write(repr(d))

        self.file.write('\n')
        self.file.flush()

class EmpytClass():
    pass

class DataFile():
    def __init__(self,Dir=''):
        self.Dir=Dir
        self.filelist=EmpytClass()#All file names are stored in this EmpytClass' attributes which will not conflict
    def In(self,filename):
        try:
            data_file=getattr(self.filelist,filename)
        except AttributeError:
            setattr(self.filelist,filename,OpenDataFile(os.path.join(self.Dir,filename)))
            data_file=getattr(self.filelist,filename)
        finally:
            return data_file