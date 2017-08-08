#!/usr/bin/env python3
import numpy,pandas
from pandas.core.frame import DataFrame

def StringToIFT(string):#translate string to int/float/tuple
    try:# translate name
        trans=eval(string)
    except NameError:# can not translate string
        trans=string
    else:
        if type(trans) not in [int,float,tuple]:# unexcepted translate
            trans=string
    return trans

class standard_form_data():
    def _AnalyseStandardLine(in_line):
        if in_line=='':
            return None
        else:
            line=in_line.strip()
            if len(line)==0:
                return '#'
            elif line[0]=='#':
                return '#'
            else:
                row=line.split('\t')
                col_name=['No.']
                value_row=[int(row[0])]
                for name_value in row[1:]:
                    nv_list=name_value.split(':')
                    col_name.append(StringToIFT(nv_list[0]))
                    value_row.append(StringToIFT(nv_list[1]))
            return DataFrame(numpy.array([value_row]),columns=col_name)
                        
    def ReadStandardData(file_name):
        Data=DataFrame({})
        f=open(file_name,'r')
        while True:
            new_line=standard_form_data._AnalyseStandardLine(f.readline())
            if type(new_line) is DataFrame:
                Data=Data.append(new_line,ignore_index=True)
            elif new_line == '#':
                continue
            elif new_line==None:
                break
        f.close()
        return Data