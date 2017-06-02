#! /usr/bin/env python3
import os,shutil
from .read.readline import readline
from .color_print import ColorPrint,UseStyle

def _GetSphenoDir():
    package_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'packages/')
    for i in os.listdir(package_dir):
        if 'SPheno' in i:
            package=os.path.join(package_dir,i)
            if os.path.isdir(package):
                print('SPheno file:\n->',package)
                return package
    else:
        print('SPheno package not found in ',package_dir)
        exit()
        
class SPheno():
    def __init__(self,
                    package_dir=_GetSphenoDir(),
                    main_routine='./bin/SPheno',
                    data_dir='mcmc/',
                    in_model='LesHouches.in'):
        if not os.path.exists(package_dir):
            ColorPrint(1,31,'','directory',package_dir,'not found, please check its path',sep=' -- ')
            exit()

        if os.path.exists(os.path.join(package_dir,main_routine)):
            print('SPheno main routine specified:\n->',os.path.join(package_dir,main_routine))
        else:
            ColorPrint(1,31,'','main program of SPheno dosen\'t exist:\n->',os.path.join(package_dir,main_routine))
            exit()

        self.package_dir=package_dir
        self.inp_model_lines=open(os.path.join(data_dir,in_model),'r').readlines()
        self.inp_dir=os.path.join(package_dir,'SPheno.in')
        self.spectr_dir=os.path.join(package_dir,'SPheno.spc.NInvSeesaw')
        self.record_dir=os.path.join(data_dir,'./record/')
        self.command=' '.join([main_routine,self.inp_dir])


        if os.path.exists(self.record_dir):
            if input(UseStyle('delete folder record? (y/n) \n',mode=1,fore=33)).upper() in ['Y','YES','']:
                shutil.rmtree(self.record_dir)
            else:
                exit('folder record/ is not deleted')
        os.mkdir(self.record_dir)

    def run(self,point):
        inp=open(self.inp_dir,'w')
        