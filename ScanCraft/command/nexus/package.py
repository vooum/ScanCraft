#!/usr/bin/env python3

import os,subprocess
from functools import partial
from .GetPackageDir import GetPackageDir
from ..operators.iterable import FlatToList

class package(object):
    def __init__(self
                ,package_name:str # Name of the package, directory name of this package should contain this string
                ,package_dir=None # Path of the package. If not given, serch the package in ./*/ScanCraft/packages/
                ,run_subdir='' # Relative(to package_dir) path where to run the package
                ,command='' # String sequence to run in shell
                ,output_file=None # Relative(to package_dir) path(or path list) of output file(s)
                ,data_format='SLHA'
                ):
        self.package_name=package_name
        if package_dir is None:
            package_dir=GetPackageDir(package_name)
        self.package_dir=package_dir
        SetDir=partial(os.path.join,self.package_dir)
        self.SetDir=SetDir
        self.run_subdir=run_subdir
        self.run_dir=SetDir(run_subdir)
        self.command=command
        self.output_file=output_file
        if type(output_file) is str:
            self.output_dir={'output':SetDir(output_file)}
        elif type(output_file) is list:
            self.output_dir=dict([(f,SetDir(f)) for f in output_file])
        elif type(output_file) is dict:
            self.output_dir=dict(
                [(key,SetDir(f)) for key,f in output_file.items()]
                )
        self.data_format=data_format
        if data_format=='SLHA':
            self.Read=None

    def Run(self,input=None,timeout=None):
        for document in self.output_dir.values():
            try: os.remove(document)
            except FileNotFoundError: pass
        run=subprocess.Popen(self.command,cwd=self.run_dir,shell=True,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        self.stdout,self.error=run.communicate(input=input,timeout=timeout)