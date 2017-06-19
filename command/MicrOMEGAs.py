#! /usr/bin/env python3

import os,shutil,subprocess
from .color_print import ColorPrint,UseStyle,Error

def _GetMicrOMEGAsDir():
    package_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'packages/')
    for i in os.listdir(package_path):
        if 'micromegas' in i:
            package=os.path.join(package_path,i)
            if os.path.isdir(package):
                print('MicrOMEGAs file:\n->',package)
                return package
    else:
        Error('MicrOMEGAs package not found in ',package_path)

class MicrOMEGAs():
    def __init__(self,
                    package_dir=None,
                    model='InV_SS',
                    main_routine='./InV_SS',
                    data_dir='mcmc/',):
        if package_dir==None:
            package_dir=_GetMicrOMEGAsDir()
        elif not os.path.exists(package_dir):
            Error('directory',package_dir,'not found, please check its path',sep=' -- ')
        
        self.package_dir=package_dir
        self.model_dir=model
        self.work_dir=os.path.join(package_dir,model)
        self.inp_file='SPheno.spc.NInvSeesaw'#------------
        self.inp_dir=os.path.join(self.work_dir,self.inp_file)
        self.output_file='omega.txt'#------------
        self.output_dir=os.path.join(self.work_dir,self.output_file)
        self.record_dir=os.path.join(data_dir,'./record/')
        self.command=' '.join([main_routine])

    def Run(self,point_file):
        shutil.copy(point_file,self.inp_dir)
        run=subprocess.Popen(self.command,
            cwd=self.work_dir,shell=True,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        run.wait()
        if (run.returncode):
            ColorPrint(0,33,'',run.communicate()[0])
            Error(run.communicate()[1])
        else:
            result=ReadFiles(self.output_dir)
        return result
    
    def Record(self,number):
        shutil.copy(self.inp_dir,os.path.join(self.record_dir,self.inp_file+'.'+str(int(number))))
