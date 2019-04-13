#! /usr/bin/env python3

# This module is only designed for SPheno package generated with SARAH.
# For different theory, name of input file, output file, and main routine are different.

# Designed by He Yangle @ htu 
#             tel:      18567561914
#             Email:    vooum@qq.com
#                       heyangle90@gmail.com
#                       heyangle@htu.edu.cn

import os,subprocess,shutil,sys,time
from ..color_print import ColorPrint,UseStyle,Error
from .GetPackageDir import GetPackageDir
from ..format.data_container import capsule
from ..read.readSLHA import ReadSLHAFile
from ..read.SLHA_string import SLHA_string
from ..operators.iterable import FlatToList

block_mapping=dict(
    [ (i,i+'IN') 
        for i in ['MSOFT','NMSSMRUN'
            ,'MSQ2','MSU2','MSD2','MSL2','MSE2','TU','TD','TE'
            ,'MUX','MV2','MX2','YV','LAMN','BMUX','TV','TLAMN'] ]
)
# Name of these blocks in input file of SPheno are suffixed with "IN".
inverse_mapping=dict([(v,k) for k,v in block_mapping.items()])

def ReadSPhenoSpectr(spectr_dir):
    try:
        result=ReadSLHAFile(spectr_dir,)
    except FileNotFoundError:
        result=capsule()
    finally:
        result.error=not bool(result.__dict__) # get no value of any parameter
    return result

class SPheno():
    block_mapping=block_mapping
    inverse_mapping=inverse_mapping

    def __init__(self,
            package_dir=None,
            input_mold='LesHouches.in.NMSSM_low',
            input_file='LesHouches.in.NMSSM_low',
            output_file='SPheno.spc.NMSSM',
            main_routine='SPhenoNMSSM',
            CleanRecord=None
        ):
        if package_dir==None:
            package_dir=GetPackageDir('SPheno')
        elif not os.path.exists(package_dir):
            Error('directory --%s-- not found, please check its path'%package_dir)

        self.package_dir=package_dir
        self.run_dir=os.path.join(package_dir,'bin')
        self.input_mold_lines=[SLHA_string(line) for line in open(input_mold).readlines()]
        self.input_file=input_file
        self.input_dir =os.path.join(self.run_dir,self.input_file)
        self.output_file=output_file
        self.output_dir=os.path.join(self.run_dir,output_file)
        self.record_dir=os.path.join(self.run_dir,'./record/')
        self.command=' '.join(['./'+main_routine,self.input_file])

        try:
            os.mkdir(self.record_dir)
        except FileExistsError:
            if CleanRecord==False:
                exit('folder record/ is not deleted')
            elif CleanRecord==None:
                if not input(UseStyle('delete folder record? (y/n) \n',mode=1,fore=34)).upper() in ['Y','YES','']:
                    exit('folder record/ is not deleted')
            elif CleanRecord.lower()=='force':
                pass
            else:
                Error('Unknown clean mode')
            shutil.rmtree(self.record_dir)
            os.mkdir(self.record_dir)
    
    def Run(self,point):
        self.SetInputFile(point)
        # ------ run
        # try: # hhh
        #     os.remove(self.output_dir)
        # except FileNotFoundError:
        #     pass

        run=subprocess.Popen(self.command,cwd=self.run_dir,shell=True,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True
        )
        while run.poll() is None:
            self.out,self.err=run.communicate()
            # time.sleep(0.01)
            
        result=self.Read(self.output_dir)
        return result

    def SetInputFile(self,point):
        inp=open(self.input_dir,'w')
        for line in self.input_mold_lines:
            semanteme=line.string.split()
            if semanteme[0].upper()=='BLOCK':
                block=semanteme[1].upper()
                par_dict=point.block_list.get( block,   # block > inverse[block] > {}
                    point.block_list.get(self.inverse_mapping.get(block),{})
                )
                try:# get type of parameter code
                    any_code=list(par_dict.keys())[0]
                except IndexError:
                    code_lenth=0
                else:
                    if isinstance(any_code,(tuple,list)):
                        code_lenth=len(any_code)
                    elif isinstance(any_code,int):
                        code_lenth=1
            elif code_lenth:
                if code_lenth==1:
                    code=int(semanteme[0])
                else:
                    code=tuple(map(int,semanteme[:code_lenth]))
                par=par_dict.get(code,None)
                # if code_lenth==1:print(code,par)
                if par:
                    inp.write(' '+' '.join(
                        list(map(str,FlatToList([code,par.value])))
                        ))
                    if line.annotation:
                        inp.write('\t# '+line.annotation)
                    if '\n' in line:
                        inp.write('\n')
                    continue
            inp.write(line)
        inp.close()
        return

    def Read(self,spectr_dir=None):
        if spectr_dir is None:
            spectr_dir=self.output_dir
        return ReadSPhenoSpectr(spectr_dir)

    def Record(self,number : int,digit_width:int=8):
        suffix=f'.{number:0>{digit_width}}'
        documents={
            'input' :os.path.join( self.record_dir, self.input_file + suffix ),
            'output':os.path.join( self.record_dir, self.output_file+ suffix )
        }
        shutil.copy( self.input_dir , documents['input'] )
        shutil.copy( self.output_dir, documents['output'])
        return documents


    def ReMake(self,Model):
            subprocess.run('make cleanall',cwd=self.package_dir,shell=True,check=True)
            # print('clean')
            subprocess.run(f'make Model={Model}',cwd=self.package_dir,shell=True
                ,check=True
                )
            # print('done')