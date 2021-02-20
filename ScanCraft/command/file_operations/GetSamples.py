#! /usr/bin/env python3
import os
from .container import capsule

def _GetNumberWithSep(file_name,number_position,separator):
    num_str=file_name.rsplit(separator,-number_position)[1] # Get number string from given position.
    return int(num_str)

def GetSampleDictWithFucn(path=None,patterns=None,number_function=None,args=dict(),raise_exception=False):
    '''
    number_position: where the number is in filename.
        eg. number_position=-2, inp.1.dat, spectr.1.dat
    '''
    if path is None: path='./'
    if isinstance(patterns,(tuple,list)):
        pass
    elif type(patterns) is str:
        patterns=[patterns]
    else:
        print('patterns should be given in list type')

    sample_dict={}
    for document in os.listdir(path):
        try: # get number from document name
            number=number_function(document,**args)
        except ValueError:
            if raise_exception:
                continue
            else:
                print(document,'jumped.')
        sample_dict.setdefault(number,capsule())
        for p in patterns:
            if p in document:
                if p in sample_dict[number]:
                    print(f"more than one files with number {number},pattern {p} found.")
                    exit()
                else:
                    sample_dict[number].update( {p:os.path.abspath(os.path.join(path,document))} )
    return sample_dict

def GetSamples(path=None,patterns=None,number_position=-1,separator='.',raise_exception=False):
    sample_dict = GetSampleDictWithFucn(
        path=path,patterns=patterns,number_function=_GetNumberWithSep
        ,args={'number_position':number_position,'separator':separator},raise_exception=raise_exception
    )
    return [sample_dict[i] for i in sorted(sample_dict.keys())]
