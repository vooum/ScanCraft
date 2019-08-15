#!/usr/bin/env python3

import os
from .package import package
from .GenerateInputFile import GenerateInputWithScan
from ..DataProcessing import SLHA_text,ReadBlock,ReadScalar
from ..operators.object import lazyprogerty

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
                 package_name='NMSSMTools_5.4.1',
                 package_dir=None,
                 input_mold='inp_mold',
                 clean=None
                ):
        self.input_mold=input_mold
        self.input_file='inp'
        self.main_routine='run'
        command=f'./{self.main_routine} {self.input_file}'
        super().__init__(package_name=package_name,
                         command=command,
                         output_file=['spectr','omega'])
        self.input_dir=self.SetDir(self.input_file)
        with open(input_mold,'r') as mold:
            self.input_mold_lines=mold.readlines()
    @lazyprogerty
    def SetInput(self):
        return GenerateInputWithScan(self.input_mold_lines,self.point,self.input_dir)
    def Run(self,point,ignore=[]):
        self.point=point
        self.SetInput(point)
        super().Run()
        output_text=[]
        with open(self.output_dir['spectr','r']) as spectr:
            for line in spectr:
                if line=='# BLOCK FINETUNING\n':
                    output_text.append(line[2:])
                else:
                    output_text.append(line)
        spectr=SLHA_text(output_text)
        return spectr