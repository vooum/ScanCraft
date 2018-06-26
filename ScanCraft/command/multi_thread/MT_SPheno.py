#!/usr/bin/env python3

import threading,sys,os,shutil,copy,time,math
from queue import Queue

from ..nexus.GetPackageDir import GetPackageDir
from ..nexus.SPheno import SPheno
from ..color_print import Error
from ..operators.iterable import FlatToList

from _thread import start_new_thread, allocate_lock

ore_lock=threading.Lock()

class SPheno_probe(threading.Thread):
    def __init__(self,ID,sequence
            ,input_mold
            ,probe_dir
            ,ReMake=None
            ,report_interval=1000
        ):
        threading.Thread.__init__(self)
        self.ID=ID
        self.probe_dir=probe_dir
        self.ReMake=ReMake
        self.report_interval=report_interval
        self.SP=SPheno(package_dir=self.probe_dir,input_mold=input_mold,CleanRecord='force')
        self.sequence=sequence

        self.sample_list = []
        self.accepted_list = []
        self.excluded_list = []
        self.number = -1


    def run(self):
        # print(self.ReMake)
        if self.ReMake:
            print(f'ReMake probe {self.ID}, Model={self.ReMake} ...')
            self.SP.ReMake(self.ReMake)
            print(f'probe {self.ID} has been ReMaked')
        while True: # sequence not empty
            ore_lock.acquire() # LOCK-----------
            if self.sequence.empty():
                ore_lock.release()
                break
            else:
                ore = self.sequence.get()
                if self.sequence.qsize() % self.report_interval == 0:
                    sys.stdout.write("  thread-%i\truning, %8i points left at %s\n" % (self.ID,self.sequence.qsize(),time.ctime()))
                ore_lock.release()
                
                sample = self.SP.Run(ore)
                
                if sample.error:
                    self.excluded_list.append(ore)
                else:
                    self.number+=1
                    # sample.documents=self.SP.Record(number)
                    sample.documents = self.SP.Record(self.number)
                    self.sample_list.append(sample)
                    self.accepted_list.append(ore)
        return




class MT_SPheno():
    def __init__(self,threads=2
            ,package_mold=None
            ,input_mold='LesHouches.in.NMSSM_low'
            ,main_routine='SPhenoNMSSM'
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
            # if input('delete folder %s? (y/n) \n'%harvest_dir).upper() in ['Y','YES','']:
            #     shutil.rmtree(harvest_dir)
            # else:
            #     exit('folder %s is remained.'%harvest_dir)
            # os.mkdir(harvest_dir)
            pass
        self.harvest_dir=harvest_dir

        self.Renew=Renew

        number_width=int(math.log10(threads))
        # for N_probe in range(threads):
        self.probes=[os.path.join(workspace,f'SPheno_{N_probe:0>{number_width}}')
                for N_probe in range(threads)
            ]

        for probe in self.probes:
            if Renew: # remove all existed SPheno copies
                try:
                    shutil.rmtree(probe)
                except FileNotFoundError:
                    pass
            try:
                shutil.copytree(package_mold, probe )
            except FileExistsError:
                    pass

    def Run(self,points:Queue,report_interval=1000,timeout=None,ReMake=None):
        if ReMake is None:
            ReMake=self.Renew
        self.SP=[]
        for ID,probe in enumerate(self.probes):
            self.SP.append(
                SPheno_probe(ID,points
                    ,self.input_mold
                    ,probe
                    ,ReMake=ReMake
                    ,report_interval=report_interval
                )
            )
        start_time = time.time()
        print('Calculations begin at %s\n  threads:\t%i\n  points:\t%i' % (time.ctime(),self.threads,points.qsize()))

        for S_i in self.SP:
            S_i.start()
        for S_i in self.SP:
            S_i.join()
        end_time = time.time()
        print('All points done. Use %f hours' % ((end_time - start_time) / 3600))

        # collect from threads
        number=-1
        self.sample_list = FlatToList([S_i.sample_list for S_i in self.SP])
        self.accepted_list = FlatToList([S_i.accepted_list for S_i in self.SP])
        self.excluded_list = FlatToList([S_i.excluded_list for S_i in self.SP])
        #  record
        self.NewRecordDir()
        for sample in self.sample_list:
            number+=1
            destinations = {
                'input'     :os.path.join(self.record_dir,'SPheno.in.' + str(number)),
                'spectrum'  :os.path.join(self.record_dir,'SPheno.out.' + str(number)),
            }
            sample.CopyTo(destinations)
        print('%i sample recorded in %s' % (number+1,self.record_dir))
    
    def NewRecordDir(self,record_pattern=None):
        self.record_time=time.strftime('_%y%m%d_%H%M%S')
        if record_pattern is None:
            record_pattern='record'
        self.record_dir=os.path.join(self.harvest_dir,record_pattern+self.record_time)
        try:
            os.mkdir(self.record_dir)
        except  FileExistsError:
            time.sleep(1)
            self.NewRecordDir()
        return