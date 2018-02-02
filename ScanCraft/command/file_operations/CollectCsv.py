#! /usr/bin/env python3
import os,pandas
from ..color_print import Error

def CollectCsvFiles(patterns=None,paths=None):
    if patterns is None:
        Error('patterns need')
    elif not isinstance(patterns,(tuple,list)):
        patterns=[patterns]
    if paths is None:
        paths=['./']
    doc_dict={}
    for pattern in patterns:
        doc_dict[pattern]={}
    for path_i in paths:
        for document in os.listdir(path_i):
            name,suffix=os.path.splitext(document)
            if suffix == '.csv':
                group,date,time=name.split('_')
                doc_dict[group][int(date)+int(time)/1000000.]=os.path.join(path_i,document)
    return doc_dict