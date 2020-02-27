#!/usr/bin/env python3

import os
from multiprocessing import Process,Queue
from ..nexus.NMSSMTools import NMSSMTools,package_name

class NTools_process(Process):
    pylon='pylon'
    def __init__(self,ID,sequence
        ,input_mold_text,package_mode_dir,package_name
        ):
        Process.__init__(self)
        self.ID=ID
        self.probe_dir=os.path.join(pylon,f'{package_name}_prob_{ID}')
        self.N = NMSSMTools(
             package_dir=self.probe_dir
            ,input_mold_text=input_mold_text
            ,record_dir=os.path.join(self.probe_dir,'record')
            )
        try:
            shutil.copytree(package_mode_dir,self.probe_dir)
        except FileExistsError:
            pass
        else:
            self.N.Make()
