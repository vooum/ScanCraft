#!/usr/bin/env python3

import os,shutil,time
from threading import Thread
from _queue import Empty
from ..nexus.NMSSMTools import NMSSMTools,package_name
from ..nexus.GetPackageDir import GetPackageDir
from ..file_operations.Rename import Tag_ctime
from ..operators.time import ChangeTime
from ..DataProcessing.data_operators.list_operators import FlatToList

class NTools_thread(Thread):
    pylon='pylon'
    def __init__(self,ID,sequence
        ,input_mold_text,package_name=package_name,package_mode_dir=None
        ):
        Thread.__init__(self)
        self.ID=ID
        self.sequence=sequence # parameter_point queue
        self.results=[]
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
            print(f'Initializing\n\tpackage name:{package_name}, ID:{ID}')
            shutil.copytree(package_mode_dir,self.probe_dir)
            self.N.Make()
        try:
            Tag_ctime(self.N.record_dir)
        except FileNotFoundError:
            pass
        finally:
            os.mkdir(self.N.record_dir)

    def run(self):
        number=-1
        self.results=[]
        while True:
            try:
                ore=self.sequence.get_nowait()
            except Empty:
                break
            else:
                number+=1
                self.N.onlyRun(ore)
                self.results.append(self.N.Record(number))
        return

    def Delete(self):
        shutil.rmtree(self.probe_dir)

class MT_NTools():
    def __init__(
        self,threads=2
        # ,workspace='Pylon'
        ,input_mold_dir='inp.dat'
        ,package_name=package_name
        ,package_mode_dir=None
        ,output_dir='./output'
        ):
        # number of threads
        self.threads=threads
        # input mold to generate input file for each point
        with open(input_mold_dir,'r') as in_mold:
            self.input_mold_text=in_mold.readlines()
        self.package_name=package_name
        self.package_mode_dir=package_mode_dir
        # folder to store output data
        try:
            print(f'old folder {output_dir} has renamed to {Tag_ctime(output_dir)}')
        except FileNotFoundError:
            pass
        finally:
            os.mkdir(output_dir)
            self.output_dir=output_dir
    def Run(self,point_queue):
        self.NTs=[]
        self.all_points=[]
        for ID in range(self.threads):
            self.NTs.append(
                NTools_thread(
                    ID,point_queue,
                    input_mold_text=self.input_mold_text,
                    package_name=self.package_name,
                    package_mode_dir=self.package_mode_dir
                )
            )
        start_time=time.time()
        total=point_queue.qsize()
        print(f'Calculations begin at {time.ctime()}\n  Threads:\t{self.threads}\n  points:\t{total}')
        
        for N_i in self.NTs:
            N_i.start()
        # overseer
        while True:
            rest=point_queue.qsize()
            print(f'running, {rest/total:.2%} queuing',end='\r')
            if rest==0:
                break
            else:
                time.sleep(1)
        for N_i in self.NTs:
            N_i.join()
        end_time=time.time()
        work_time=ChangeTime(end_time-start_time)
        print(f'All points done. Use {work_time}')

        self.all_points=FlatToList(
            [N_i.results for N_i in self.NTs]
        )
        print('all data files stored in \'all_points\' attribute')
        return self.all_points

    def DeleteData(self):
        for record_dir in [NT.N.record_dir for NT in self.NTs]:
            try:
                shutil.rmtree(record_dir)
            except FileNotFoundError:
                pass