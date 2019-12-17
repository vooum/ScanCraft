#!/usr/bin/env python3

import os,shutil
from .package import package
from .GenerateInputFile import GenerateInputWithScan
from ..DataProcessing import SLHA_text,ReadBlock,ReadScalar
from ..operators.object import lazyproperty

# Read spectial blocks of NMSSMTools
class NTools_block_format(ReadBlock):
    LHCCROSSSECTIONS=ReadScalar
    DELTAMH=ReadScalar
    LOWEN=ReadScalar
    
    @staticmethod
    def SPINFO(lines):
        data={}
        for line in lines:
            code=line.strip()[0]
            if code in ['3','4']:
                data.setdefault(int(code),[]).append(line.split('#')[1])
        return data

def ReadNToolsOutput(spectr_dir,*omega_dir,ignore=[]):
    return NToolsOutput(spectr_dir,*omega_dir,ignore=[])

class NToolsOutput(SLHA_text):
    def __init__(self,spectr_dir,*omega_dir,ignore=[]):
        self.spectr_dir=spectr_dir
        self.ignore=ignore
        output_text=[] 
        with open(spectr_dir,'r') as spectr:
            for line in spectr:
                if line=='# BLOCK FINETUNING\n':
                    output_text.append(line[2:])
                else:
                    output_text.append(line)
        try:
            with open(omega_dir[0],'r') as omega:
                output_text.extend(omega.readlines())
        except FileNotFoundError:
            pass
        except IndexError:
            pass
        else:
            self.omega_dir=omega_dir[0]
        super().__init__(output_text,block_format=NTools_block_format)
    @property
    def constraints(self):
        all_consts=[]
        for constraint in self.BLOCK.SPINFO[3]:
            for const in self.ignore:
                if const in constraint:
                    break
            else:
                all_consts.append(constraint)
        return all_consts
    @property
    def error(self):
        return not bool(self.constraints)


class NMSSMTools(package):
    def __init__(self,
                 package_name='NMSSMTools_5.4.1',
                 package_dir=None,
                 input_mold='inp_mold',
                 record_dir='./output/record/',
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

        self.record_dir=record_dir
    @lazyproperty
    def SetInput(self):
        return GenerateInputWithScan(self.input_mold_lines,self.point,self.input_dir)
    def Run(self,point,ignore=[]):
        self.point=point
        self.SetInput(point)
        super().Run()
        return ReadNToolsOutput(self.output_dir['spectr'],self.output_dir['omega'],ignore=ignore)
    def Record(self,number):
        destinations={
            'input'     :os.path.join(self.record_dir,f'inp.{number}'),
            'spectrum'  :os.path.join(self.record_dir,f'spectr.{number}'),
            'omega'     :os.path.join(self.record_dir,f'omega.{number}')
        }
        shutil.copy(self.input_dir,destinations['input'])
        shutil.copy(self.output_dir['spectr'],destinations['spectrum'])
        try:
            shutil.copy(self.output_dir['omega'],destinations['omega'])
        except FileNotFoundError:
            pass