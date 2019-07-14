#!/usr/bin/env python3

import os
from .GetPackageDir import GetPackageDir

class package(object):
    def __init__(self
                ,package_name:str # Name of the package, directory name of this package should contain this string
                ,package_dir=None # Path of the package. If not given, serch the package in ./*/ScanCraft/packages/
                ,run_subdir='./' # Relative(to package_dir) path where to run the package
                ,command # String sequence to run in shell
                ,output_file=None # Relative(to package_dir) path(or path list) of output file(s)
                ):
        self.package_name=package_name
        if package_dir is None:
            self.package_dir=GetPackageDir(package_name)
        self.run_subdir=run_subdir
        self.run_dir=os.path.join(self.package_dir,run_subdir)
        self.command=command
        self.output_file=output_file
    def _Run(self):
        run=subprocess.Popen(self.command,cwd=self.run_dir,shell=True,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)