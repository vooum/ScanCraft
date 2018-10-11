#!/usr/bin/env python3
'''
Read MicrOMEAGs output files written by Stau's main porgram
    including omg.out & channels.out.
Caution: 
    '%li' in the main program:
    'CalcOmega_with_DDetection_MOv5.cpp' 
    should be substitute to '%i' 
    so -1 will not be converted to 4294967295
'''
import os
from .GetPackageDir import GetPackageDir

class MicrOMEAGs(object):
    def __init__(self
                ,package_dir=None
                ,run_path='NMSSM'
                ,main_routine='CalcOmega_with_DDetection_MOv5'
        ):
        if package_dir==None:
            package_dir=GetPackageDir('micromegas')
        elif not os.path.exists(package_dir):
            Error('directory --%s-- not found, please check its path'%package_dir)
        self.package_dir=package_dir
        self.run_dir=os.path.join(package_dir,run_file)
        