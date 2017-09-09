#! /usr/bin/env python3
import os,re,sys
def GetFiles(address,similarity=''):
    file_list=[]
    candidate={}
    total=0
    for document in os.listdir(address):
        if similarity in document:
            try:
                number=int(re.findall(r'\d+',document)[-1])
            except IndexError:
                continue
            else:
                candidate.update({number:document})
                total +=1
    # for i in sorted(candidate.keys()):
        # file_list.append(os.path.join(os.getcwd(),address,document))
    if total !=len(candidate.keys()):
        exit('number conflict')
    # file_list=[os.path.join(os.getcwd(),address,candidate[i]) for i in  sorted(candidate.keys())]
    file_list=[os.path.abspath(os.path.join(address,candidate[i])) for i in sorted(candidate.keys())]
    return file_list