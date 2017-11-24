#!/usr/bin/env python3
import threading,sys,os,shutil,queue,copy
from ..NMSSMTools import NMSSMTools


ore_lock=threading.Lock()
number_lock=threading.Lock()

class NTools_thread(threading.Thread):
    def warp(number):
    position='./Pylon/prob'+str(number)
    try:
        shutil.copytree('./Pylon/prob/',position)
    except FileExistsError:
        pass
    N=NMSSMTools(package_dir=position,data_dir=position,in_model='./Pylon/inpZ3.dat',clean=False)
    return N

    def __init__(self,ID,sequence):
        threading.Thread.__init__(self)
        self.ID=ID
        self.N=warp(ID)
        self.sequence=sequence
        self.sample_list=[]
        self.accepted_list=[]
        self.excluded_list=[]
        self.number=-1
    def run(self):
        while not self.sequence.empty():
            ore_lock.acquire() # LOCK-----------
            ore=self.sequence.get()
            # sys.stdout.write(' '.join([
            #     repr(i) for i in [self.ID,'runing',ore.variable_list['tanB'].value,'at',time.ctime()]
            #     ])+'\n')
            if self.sequence.qsize()%100==0:
                sys.stdout.write("%3i runing, %8i points left at %s\n"%(self.ID,self.sequence.qsize(),time.ctime()))
            ore_lock.release()
            
            sample=self.N.Run(ore)
            
            if len(sample.SPINFO[4])==0:
                self.sample_list.append(sample)
                self.accepted_list.append(ore)
                self.number+=1
                sample.document={'number',self.number}
                sample.update(self.N.Record(self.number))
                # sys.stdout.write(' '.join([
                #     repr(i) for i in [self.ID,'done',sample.MINPAR,'at',time.ctime(),len(self.sample_list)]
                #     ])+'\n')
            else:
                self.excluded_list.append(ore)
                # sys.stdout.write(' '.join([
                #     repr(i) for i in [self.ID,'excluded',sample.MINPAR[3],'at',time.ctime(),sample.SPINFO]
                #     ])+'\n')

            # number_lock.acquire() # LOCK-----------
            # number_lock.release()
    def Clean(self):
        shutil.rmtree(self.N.record_dir)
        os.mkdir(self.N.record_dir)

class MT_NTools(sequence):
    def __init__()