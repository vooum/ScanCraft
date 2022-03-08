#! /usr/bin/env python3
import os,pandas

def CollectCsvFiles(keywords=None,paths=None):
    if keywords is None:
        print('\033[1;31;40mpatterns need\033[0m')
        exit()
    elif not isinstance(keywords,(tuple,list)):
        keywords=[keywords]

    if paths is None:
        paths=['./']
    doc_dict={}
    for pattern in keywords:
        doc_dict[pattern]={}
    for path_i in paths:
        for document in os.listdir(path_i):
            name,suffix=os.path.splitext(document)
            if suffix == '.csv':
                group,date,time=name.split('_')
                doc_dict[group][int(date)+int(time)/1000000.]=os.path.join(path_i,document)
    return doc_dict