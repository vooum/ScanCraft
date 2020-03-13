#!/usr/bin/env python3

import os,shutil,subprocess
from .package import package
from .GenerateInputFile import GenerateInputWithScan
from ..DataProcessing import SLHA_text,ReadBlock,ReadScalar
from ..operators.object import lazyproperty

# package version:
package_name='NMSSMTools_5.5.2'

# Read spectial blocks of NMSSMTools
class NTools_block_format(ReadBlock):
    LHCCROSSSECTIONS=ReadScalar
    DELTAMH=ReadScalar
    LOWEN=ReadScalar
    
    @staticmethod
    def SPINFO(lines):
        info={}
        item=['']
        # last_code=0
        for line in lines:
            # print(line,item,last_code)
            try:
                code=int(line.split(maxsplit=1)[0])
            except ValueError:
                item[-1]+' '+line.strip()
            else:
                item=info.setdefault(int(code),[])
                message=line.split(maxsplit=1)[1].strip()
                item.append(message)
                # last_code=code
        return info

def ReadNToolsOutput(spectr_dir,*omega_dir,ignore=[]):
    return NToolsOutput(spectr_dir,*omega_dir,ignore=ignore)

class NToolsOutput(SLHA_text):
    def __init__(self,spectr_dir=None,omega_dir=None,text=None,ignore=[]):
        self.ignore=ignore
        output_text=[]
        if spectr_dir:
            with open(spectr_dir,'r') as spectr:
                for line in spectr:
                    if line=='# BLOCK FINETUNING\n':
                        output_text.append(line[2:])
                    else:
                        output_text.append(line)
            self.spectr_dir=spectr_dir
        if omega_dir:
            with open(omega_dir,'r') as omega:
                output_text.extend(omega.readlines())
            self.omega_dir=omega_dir[0]
        if text:
            for line in text:
                if line=='# BLOCK FINETUNING\n':
                    output_text.append(line[2:])
                else:
                    output_text.append(line)
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
        return 4 in self.BLOCK.SPINFO


class NMSSMTools(package):
    input_file='inp'
    main_routine='run'
    def __init__(self,
                 package_name=package_name,
                 package_dir=None,
                 input_mold:str='',
                 input_mold_text:list=[],
                 record_dir='./output/record/',
                 clean=None
                ):
        self.input_mold_text=input_mold_text
        self.input_mold=input_mold
        if input_mold:
            if input_mold_text:
                print('input_mold_text is already given, input_mold not needed')
            else:
                with open(input_mold,'r') as mold:
                    self.input_mold_text=mold.readlines()
        command=f'./{self.main_routine} {self.input_file}'
        super().__init__(package_name=package_name,
                         package_dir=package_dir,
                         command=command,
                         data_file=['inp','spectr','omega'])

        self.record_dir=record_dir
    
    @lazyproperty
    def SetInput(self):
        return GenerateInputWithScan(self.input_mold_text,self.point,self.data_dir['inp'])
    
    def onlyRun(self,point,ignore=[]):
        self.point=point
        self.SetInput(point)
        super().Run()
        return

    def Run(self,point,ignore=[]):
        self.onlyRun(self,point,ignore=ignore)
        return NToolsOutput(self.data_dir['spectr'],self.data_dir['omega'],ignore=ignore)
    
    def Record(self,number):
        destinations={
            'inp'     :os.path.join(self.record_dir,f'inp.{number}'),
            'spectr'  :os.path.join(self.record_dir,f'spectr.{number}'),
            'omega'     :os.path.join(self.record_dir,f'omega.{number}')
        }
        new_capsule=self.data_dir.CopyTo(destinations)
        # shutil.copy(self.data_dir['inp'],destinations['input'])
        # shutil.copy(self.data_dir['spectr'],destinations['spectrum'])
        # try:
        #     shutil.copy(self.data_dir['omega'],destinations['omega'])
        # except FileNotFoundError:
        #     del destinations['omega']
        return new_capsule
    
    def Make(self):
        log_file=os.path.join(self.package_dir,'setup_log.txt')
        with open(log_file,'w') as log:
            run=subprocess.run('make init',
                stdout=log, stderr=log ,cwd=self.package_dir, shell=True)
            run=subprocess.run('make',
                stdout=log, stderr=log, cwd=self.package_dir, shell=True)
    
    def Clean(self):
        log_file=os.path.join(self.package_dir,'clean_log.txt')
        with open(log_file,'w') as log:
            run=subprocess.Popen('make clean',
                stdin=subprocess.PIPE, stdout=log, stderr=log, cwd=self.package_dir, shell=True)
            run.communicate(b'y\ny\n')
        if run.returncode==0:
            print('clean done')
        else:
            print('err in clean, return code:', run.returncode)