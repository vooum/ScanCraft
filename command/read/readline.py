#!/usr/bin/env python3


def readline(line):
    constituents=[]
    annotation=[False]
    if line.strip(' \n')[0]=='#':
        annotation=[True]
    constituents=line.lstrip(' #').rstrip(' \n').split('#',maxsplit=1)
    a=constituents
    constituents.extend(annotation)
    return a



if __name__=='__main__':
    string='a# #a #\n'
    print(readline(string))