#!/usr/bin/env python3
import threading,sys,os,shutil,queue,copy,time
from ..NMSSMTools import NMSSMTools
from ..color_print import Error
from ..format.data_structure_functions import FlatToList

ore_lock = threading.Lock()
number_lock = threading.Lock()

class NTools_thread(threading.Thread):
    def __init__(self,ID,sequence
                ,pylon='Pylon'
                ,input_mold='./Pylon/inpZ3.dat'
                ,probe_mold='./Pylon/probe'):
        threading.Thread.__init__(self)
        self.ID = ID
        self.probe = os.path.join(pylon,'probe' + str(ID))
        try:
            shutil.copytree(probe_mold,self.probe)
        except FileExistsError:
            pass
        self.N = NMSSMTools(package_dir=self.probe,data_dir=self.probe,input_mold='./Pylon/inpZ3.dat',clean='force')
        self.sequence = sequence
        self.sample_list = []
        self.accepted_list = []
        self.excluded_list = []
        self.number = -1
    def run(self):
        while True:  #not self.sequence.empty():
            ore_lock.acquire() # LOCK-----------
            if self.sequence.empty():
                ore_lock.release()
                break
            else:
                ore = self.sequence.get()
                if self.sequence.qsize() % 1000 == 0:
                    sys.stdout.write("  thread-%i\truning, %8i points left at %s\n" % (self.ID,self.sequence.qsize(),time.ctime()))
                ore_lock.release()
                
                sample = self.N.Run(ore)
                
                if len(sample.SPINFO[4]) == 0:
                    self.number+=1
                    sample.documents = self.N.Record(self.number)
                    self.sample_list.append(sample)
                    self.accepted_list.append(ore)
                else:
                    self.excluded_list.append(ore)
        # print(self.ID,'stop')
        return

class MT_NTools():
    def __init__(self,threads=2
            ,workspace='Pylon'
            ,input_mold='inpZ3,dat'
            ,package_mold='./Pylon/probe'
            ,output_dir='./output'
            #,record_dir=None
            ):

        try:
            os.mkdir(output_dir)
        except FileExistsError:
            if input('delete folder %s? (y/n) \n'%output_dir).upper() in ['Y','YES','']:
                shutil.rmtree(output_dir)
            else:
                exit('folder %s is remained.'%output_dir)
            os.mkdir(output_dir)
        self.output_dir=output_dir
        # self.record_dir = record_dir

        if os.path.isfile(input_mold):#find input file mold
            self.input_mold = input_mold
        else:
            inp2 = os.path.join(workspace,input_mold)
            if not os.path.isfile(inp2):
                self.input_mold = inp2
            else:
                Error('%s not found in ./ or %s' % (input_mold,inp2))

        self.threads = threads
        self.workspace = workspace
        self.package_mold = package_mold

    def Run(self,point_queue,timeout=None):
        self.NT = []
        for ID in range(self.threads):
            self.NT.append(NTools_thread(ID,point_queue
                            ,pylon=self.workspace
                            ,input_mold=self.input_mold
                            ,probe_mold=self.package_mold))
        start_time = time.time()
        print('Calculations begin at %s\n  threads:\t%i\n  points:\t%i' % (time.ctime(),self.threads,point_queue.qsize()))

        for N_i in self.NT:
            N_i.start()
        for N_i in self.NT:
            N_i.join(timeout=timeout)
        end_time = time.time()
        print('All points done. Use %f hours' % ((end_time - start_time) / 3600))

        # collect from threads
        number = -1
        self.sample_list = FlatToList([N_i.sample_list for N_i in self.NT])
        self.accepted_list = FlatToList([N_i.accepted_list for N_i in self.NT])
        self.excluded_list = FlatToList([N_i.excluded_list for N_i in self.NT])

        # record
        self.NewRecordDir()
        for sample in self.sample_list:
            number+=1
            destinations = {
                'input'     :os.path.join(self.record_dir,'inp.dat.' + str(number)),
                'spectrum'  :os.path.join(self.record_dir,'spectr.dat.' + str(number)),
                'omega'     :os.path.join(self.record_dir,'omega.dat.' + str(number))
            }
            sample.CopyTo(destinations)
        print('%i sample recorded in %s' % (number+1,self.record_dir))

    def NewRecordDir(self,record_pattern=None):
        self.record_time=time.strftime('_%y%m%d_%H%M%S')
        if record_pattern is None:
            record_pattern='record'
        self.record_dir=os.path.join(self.output_dir,record_pattern+self.record_time)
        try:
            os.mkdir(self.record_dir)
        except  FileExistsError:
            time.sleep(1)
            self.NewRecordDir()
        return
