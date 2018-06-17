#!/usr/bin/env python3

import threading,sys,os,shutil,copy,time,math
from queue import Queue

from ..nexus.GetPackageDir import GetPackageDir
from ..nexus.SPheno import SPheno
from ..color_print import Error
from ..format.data_structure_functions import FlatToList

from _thread import start_new_thread, allocate_lock

ore_lock=threading.Lock()

class SPheno_probe(threading.Thread):
    def __init__(self,ID,sequence
            ,input_mold
            ,probe_dir
            ,ReMake=False
        ):
        threading.Thread.__init__(self)
        self.ID=ID
        self.probe_dir=probe_dir
        self.ReMake=ReMake
        self.SP=SPheno(package_dir=self.probe_dir,input_mold=input_mold,CleanRecord='force')
        self.sequence=sequence

        self.sample_list = []
        self.accepted_list = []
        self.excluded_list = []
        self.number = -1


    def run(self):
        print(self.ReMake)
        if self.ReMake:
            print(f'ReMake probe {self.ID}...')
            self.SP.ReMake()
            print(f'probe {self.ID} has been ReMaked')
        while True: # sequence not empty
            ore_lock.acquire() # LOCK-----------
            if self.sequence.empty():
                ore_lock.release()
                break
            else:
                ore = self.sequence.get()
                if self.sequence.qsize() % 1000 == 0:
                    sys.stdout.write("  thread-%i\truning, %8i points left at %s\n" % (self.ID,self.sequence.qsize(),time.ctime()))
                ore_lock.release()
                
                sample = self.SP.Run(ore)
                
                if sample.error:
                    self.excluded_list.append(ore)
                else:
                    self.number+=1
                    sample.documents = self.SP.Record(self.number)
                    self.sample_list.append(sample)
                    self.accepted_list.append(ore)
        return




class MT_SPheno():
    def __init__(self,threads=2
            ,package_mold=None
            ,input_mold='LesHouches.in.NMSSM_low'
            ,workspace='Pylon'
            ,harvest_dir='./output'
            ,Renew=False
        ):

        self.threads=threads

        if package_mold is None:
            package_mold=GetPackageDir('SPheno')
        elif not os.path.exists(package_mold):
            Error('directory --%s-- not found, please check its path'%package_dir)
        # self.package_mold=package_mold

        self.input_mold = input_mold

        self.workspace=workspace
        try:
            os.mkdir(workspace)
        except FileExistsError:
            pass

        try:# creat fold which will contain all output documents
            os.mkdir(harvest_dir)
        except FileExistsError:
            if input('delete folder %s? (y/n) \n'%harvest_dir).upper() in ['Y','YES','']:
                shutil.rmtree(harvest_dir)
            else:
                exit('folder %s is remained.'%harvest_dir)
            os.mkdir(harvest_dir)
        self.harvest_dir=harvest_dir

        self.Renew=Renew

        number_width=int(math.log10(threads))
        # for N_probe in range(threads):
        self.probes=[os.path.join(workspace,f'SPheno_{N_probe:0>{number_width}}')
                for N_probe in range(threads)
            ]
        for probe in self.probes:
            try:
                shutil.copytree(package_mold, probe )
            except FileExistsError:
                pass


    def Run(self,points:Queue,timeout=None,ReMake=False):
        self.SP=[]
        for ID,probe in enumerate(self.probes):
            self.SP.append(
                SPheno_probe(ID,points
                    ,self.input_mold
                    ,probe
                    ,ReMake=ReMake
                )
            )
        for S_i in self.SP:
            S_i.start()
        for S_i in self.SP:
            S_i.join()
        print('done')