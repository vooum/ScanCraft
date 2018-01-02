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
        while not self.sequence.empty():
            ore_lock.acquire() # LOCK-----------            
            ore = self.sequence.get()
            # sys.stdout.write(' '.join([
            #     repr(i) for i in
            #     [self.ID,'runing',ore.variable_list['tanB'].value,'at',time.ctime()]
            #     ])+'\n')
            if self.sequence.qsize() % 100 == 0:
                sys.stdout.write("  thread-%i\truning, %8i points left at %s\n" % (self.ID,self.sequence.qsize(),time.ctime()))
            ore_lock.release()
            
            sample = self.N.Run(ore)
            
            if len(sample.SPINFO[4]) == 0:
                self.number+=1
                sample.documents = self.N.Record(self.number)
                self.sample_list.append(sample)
                self.accepted_list.append(ore)
                # sys.stdout.write(' '.join([
                #     repr(i) for i in
                #     [self.ID,'done',sample.MINPAR,'at',time.ctime(),len(self.sample_list)]
                #     ])+'\n')
            else:
                self.excluded_list.append(ore)
                
                # sys.stdout.write(' '.join([
                #     repr(i) for i in
                #     [self.ID,'excluded',sample.MINPAR[3],'at',time.ctime(),sample.SPINFO]
                #     ])+'\n')
    def Clean(self):
        shutil.rmtree(self.N.record_dir)
        os.mkdir(self.N.record_dir)

class MT_NTools():
    def __init__(self,threads=2
            ,work_space='Pylon'
            ,input_mold='inpZ3,dat'
            ,package_mold='./Pylon/probe'
            ,record_dir='./Pylon/record'): 

        try:
            os.mkdir(record_dir)
        except FileExistsError:
            if input('delete folder record? (y/n) \n').upper() in ['Y','YES','']:
                shutil.rmtree(record_dir)
            else:
                exit('folder record/ is not deleted')
            os.mkdir(record_dir)
        self.record_dir = record_dir  

        if os.path.isfile(input_mold):
            self.input_mold = input_mold
        else:
            inp2 = os.path.join(work_space,input_mold)
            if not os.path.isfile(inp2):
                self.input_mold = inp2
            else:
                Error('%s not found in ./ or %s' % (input_mold,inp2))

        self.threads = threads
        self.work_space = work_space
        self.package_mold = package_mold

    def Run(self,point_queue,timeout=None):
        self.NT = []
        for ID in range(self.threads):
            self.NT.append(NTools_thread(ID,point_queue
                            ,pylon=self.work_space
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
        # return NT
        number = -1
        self.sample_list = FlatToList([N_i.sample_list for N_i in self.NT])
        self.accepted_list = FlatToList([N_i.accepted_list for N_i in self.NT])
        self.excluded_list = FlatToList([N_i.excluded_list for N_i in self.NT])
        for sample in self.sample_list:
            number+=1
            destinations = {
                'input'     :os.path.join(self.record_dir,'inp.dat.' + str(number)),
                'spectrum'  :os.path.join(self.record_dir,'spectr.dat.' + str(number)),
                'omega'     :os.path.join(self.record_dir,'omega.dat.' + str(number))
            }
            sample.CopyTo(destinations)
        print('%i sample recorded in %s' % (number+1,self.record_dir))
