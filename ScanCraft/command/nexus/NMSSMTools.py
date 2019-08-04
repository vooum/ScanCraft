#!/usr/bin/env python3

from .package import package
from ..DataProcessing import *

# Read spectial blocks of NMSSMTools
class ReadNToolsSpectr(ReadBlock):
    LHCCROSSSECTIONS=ReadScalar
    DELTAMH=ReadScalar
    @staticmethod
    def SPINFO(lines):
        data={}
        for line in lines:
            code=line.strip()[0]
            if code in ['3','4']:
                data.setdefault(int(code),[]).append(line.split('#')[1])
        return data

class NMSSMTools(package):
    def __init__(self,
                 package_name='NMSSMTools_5.4.1'
                 package_dir=None,
                 input_mold='inp_mold',
                 clean=None
                ):
        self.input_file='inp'
        self.main_routine='run'
        command=f'./{self.main_routine} {self.input_file}'
        super().__init__(package_name=package_name,
                         command=command,
                         output_file=['spectr','omega'])
        with open(self.input_mold,'r') as mold:
            self.input_mold_lines=mold.readlines()



    def Run(self,point,ignore=[]):
