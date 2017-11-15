#! /usr/bin/env python3
import os,re,sys
def GetFiles(address,similarity='',HasNumber=True):
    file_list=[]
    candidate={}
    total=0
    for document in os.listdir(address):
        if similarity in document:
            try:
                number=int(re.findall(r'\d+',document)[-1])
            except IndexError:
                if HasNumber:continue
                else:candidate.update({-1-total:document})
            else:
                candidate.update({number:document})
            finally:
                total +=1
    # for i in sorted(candidate.keys()):
        # file_list.append(os.path.join(os.getcwd(),address,document))
    if total !=len(candidate.keys()):
        print(candidate,total)
        exit('number conflict')
    # file_list=[os.path.join(os.getcwd(),address,candidate[i]) for i in  sorted(candidate.keys())]
    file_list=[os.path.abspath(os.path.join(address,candidate[i])) for i in sorted(candidate.keys())]
    return file_list