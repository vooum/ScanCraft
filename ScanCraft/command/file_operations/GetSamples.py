#! /usr/bin/env python3
import os
from ..format.data_container import capsule
from ..color_print import Error

def GetSamples(argv=None,patterns=None,path=None):
    if path is None: path='./'
    if patterns is None:
        Error('pattern of files empty')
    else:
        if not isinstance(patterns,(tuple,list)):patterns=[patterns]
    sample_dict={}
    for document in os.listdir(path):
        try:# document not numbered
            name,suffix=document.rsplit('.',1)
        except ValueError:
            continue

        try:# suffix must be a integer
            suffix=int(suffix)
        except ValueError:
            continue

        if suffix not in sample_dict:
            sample_dict.update({ suffix:capsule() })
            setattr( sample_dict[suffix], 'documents', {})
        for p in patterns:
            if p in name:
                if p in sample_dict[suffix].documents:
                    Error("more than one files with pattern '%s' found")
                else:
                    sample_dict[suffix].documents.update( {p:os.path.abspath(os.path.join(path,document))} )

    return [sample_dict[i] for i in sorted(sample_dict.keys())]



