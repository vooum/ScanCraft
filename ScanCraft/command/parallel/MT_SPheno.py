#!/usr/bin/env python3

import threading,sys,os,shutil,copy,time,math
from queue import Queue

from ..nexus.GetPackageDir import GetPackageDir
from ..nexus.SPheno import SPheno
from ..nexus.Higgs_Bounds_and_Signals import HiggsBounds
from ..color_print import Error
from ..operators.iterable import FlatToList

from ..data_transformer.InputToPandas import InputToPandas

ore_lock=threading.Lock()

class SPheno_probe(threading.Thread):
    def __init__(self,ID,sequence
            ,probe_dir
            ,input_mold='LesHouches.in.NMSSM_low'
            ,input_file='LesHouches.in.NMSSM_low'
            ,output_file='SPheno.spc.NMSSM'
            ,main_routine='SPhenoNMSSM'
            ,ReMake=None
            ,report_interval=1000
        ):
        threading.Thread.__init__(self)
        self.ID=ID
        self.probe_dir=probe_dir
        self.ReMake=ReMake
        self.report_interval=report_interval
        self.SP=SPheno(package_dir=probe_dir
                ,input_mold=input_mold
                ,input_file=input_file
                ,output_file=output_file
                ,main_routine=main_routine
                ,CleanRecord='force')
        self.HB=HiggsBounds(target_dir=self.SP.run_dir,mode='SARAH',silent=True)
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
                
                try:
                    sample = self.SP.Run(ore)
                except FileNotFoundError:
                    self.excluded_list.append(ore)
                    continue
                
                if sample.error:
                    self.excluded_list.append(ore)
                else:
                    self.number+=1
                    # run HiggsBounds
                    HB=self.HB.RunSARAH()
                    sample.HBresult={'HBresult':HB.HBresult,'obsratio':HB.obsratio}
                    
                    sample.documents = self.SP.Record(self.number)
                    sample.documents.update(self.HB.Record(self.number,record_dir=self.SP.record_dir))

                    N_sample=len(self.sample_list)
                    if N_sample % 100 ==0:
                        sys.stdout.write(f'Thread-{self.ID} got {N_sample} samples\n')

                    self.sample_list.append(sample)
                    self.accepted_list.append(ore)
        return




class MT_SPheno():
    def __init__(self,threads=2
            ,package_mold=None
            ,input_mold='LesHouches.in.NMSSM_low'
            ,input_file='LesHouches.in.NMSSM_low'
            ,output_file='SPheno.spc.NMSSM'
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
        self.input_file = input_file
        self.output_file= output_file
        self.main_routine=main_routine

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
        self.SP_threads=[]
        for ID,probe in enumerate(self.probes):
            self.SP_threads.append(
                SPheno_probe(ID,points
                    ,probe_dir=probe
                    ,input_mold=self.input_mold
                    ,input_file=self.input_file
                    ,output_file=self.output_file
                    ,main_routine=self.main_routine
                    ,ReMake=ReMake
                    ,report_interval=report_interval
                )
            )
        start_time = time.time()
        print('Calculations begin at %s\n  threads:\t%i\n  points:\t%i' % (time.ctime(),self.threads,points.qsize()))

        for S_i in self.SP_threads:
            S_i.start()
        for S_i in self.SP_threads:
            S_i.join()

        end_time = time.time()
        print('All points done. Use %f hours' % ((end_time - start_time) / 3600))

        # collect from threads
        number=-1
        self.sample_list = FlatToList([S_i.sample_list for S_i in self.SP_threads])
        self.accepted_list = FlatToList([S_i.accepted_list for S_i in self.SP_threads])
        self.excluded_list = FlatToList([S_i.excluded_list for S_i in self.SP_threads])
        #  record
        self.NewRecordDir()
        if len(self.sample_list)==0:
            os.rmdir(self.record_dir)
            return
        for sample in self.sample_list:
            number+=1
            destinations = {
                'input'     :os.path.join(self.record_dir,'SPheno.in.' + str(number)),
                'output'  :os.path.join(self.record_dir,'SPheno.out.' + str(number)),
            }
            sample.CopyTo(destinations)
        print('%i sample recorded in %s' % (number+1,self.record_dir))
        return
        if self.excluded_list:
            excluded_pdx=InputToPandas(self.excluded_list,title='excluded')
            excluded_pdx.to_csv(os.path.join(self.harvest_dir,f'excluded_{self.record_time}.csv'))
    
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
