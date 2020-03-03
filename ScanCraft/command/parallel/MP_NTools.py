#!/usr/bin/env python3

import os,shutil,time
from multiprocessing import Process,Queue
from ..nexus.NMSSMTools import NMSSMTools,package_name
from ..nexus.GetPackageDir import GetPackageDir

class NTools_process(Process):
    pylon='pylon'
    def __init__(self,ID,sequence
        ,input_mold_text,package_name,package_mode_dir=None
        ):
        Process.__init__(self)
        self.ID=ID
        self.sequence=sequence # parameter_point queue
        if package_mode_dir is None:
            package_mode_dir=GetPackageDir(package_name,silent=True)
        self.package_mode_dir=package_mode_dir
        self.probe_dir=os.path.join(self.pylon,f'{package_name}_prob_{ID}')
        self.N = NMSSMTools(
             package_dir=self.probe_dir
            ,input_mold_text=input_mold_text
            ,record_dir=os.path.join(self.probe_dir,'record')
            )
        if not os.path.isdir(self.probe_dir):
            shutil.copytree(package_mode_dir,self.probe_dir)
            self.N.Make()
        if os.path.exists(self.N.record_dir):
            Now=time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            dest=self.N.record_dir+'_copied_at_'+Now
            shutil.move(self.N.record_dir,dest)
        os.mkdir(self.N.record_dir)

    def run(self):
        number=-1
        while True:
            try:
                ore=self.sequence.get_nowait()
            except Empty:
                break
            else:
                number+=1
                sample=self.N.Run(ore)
                if not sample.error:
                    self.N.Record(number)
        return

    def Delete(self):
        shutil.rmtree(self.probe_dir)

class MP_NTools():
    def __init__(
        self,processes=2
        # ,workspace='Pylon'
        ,input_mold_dir='inp.dat'
        ,package_name=package_name
        ,output_dir='./output'
        ):
        try:
            os.mkdir(output_dir)
        except FileExistsError:
            pass