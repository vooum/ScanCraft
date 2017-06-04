#! /usr/bin/env python3
import os,shutil,subprocess
from .data_type import scalar,matrix
from .read.readline import commented_out,ReadLine
from .read.readSLHA import ReadFiles
from .color_print import ColorPrint,UseStyle,Error

def _GetSphenoDir():
    package_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'packages/')
    for i in os.listdir(package_path):
        if 'SPheno' in i:
            package=os.path.join(package_path,i)
            if os.path.isdir(package):
                print('SPheno file:\n->',package)
                return package
    else:
        print('SPheno package not found in ',package_path)
        exit()
        
class SPheno():
    def __init__(self,
                    package_dir=None,
                    main_routine='./bin/SPheno',
                    data_dir='mcmc/',
                    in_model='LesHouches.in'):
        if package_dir==None:
            package_dir=_GetSphenoDir()
        elif not os.path.exists(package_dir):
            Error('directory',package_dir,'not found, please check its path',sep=' -- ')

        if os.path.exists(os.path.join(package_dir,main_routine)):
            print('SPheno main routine specified:\n->',os.path.join(package_dir,main_routine))
        else:
            Error('main program of SPheno dosen\'t exist:\n->',os.path.join(package_dir,main_routine))

        self.package_dir=package_dir
        self.inp_model_lines=open(os.path.join(data_dir,in_model),'r').readlines()
        self.inp_file='SPheno.in'
        self.inp_dir=os.path.join(package_dir,self.inp_file)
        self.spectr_dir=os.path.join(package_dir,'SPheno.spc.NInvSeesaw')
        self.record_dir=os.path.join(data_dir,'./record/')
        self.command=' '.join([main_routine,self.inp_file])


        if os.path.exists(self.record_dir):
            if input(UseStyle('delete folder record? (y/n) \n',mode=1,fore=34)).upper() in ['Y','YES','']:
                shutil.rmtree(self.record_dir)
            else:
                exit('folder record/ is not deleted')
        os.mkdir(self.record_dir)

    def run(self,point):
        # write input file for SPheno
        code_list={}
        inp=open(self.inp_dir,'w')
        for line in self.inp_model_lines:
            if not commented_out(line):
                semanteme=ReadLine(line)
                if str(semanteme[0]).upper()=='BLOCK':
                    if semanteme[1] in point.block_list.keys():
                        block_i=point.block_list[semanteme[1]]
                        if type(block_i) is dict:
                            code_lenth=1
                            for PDG,p_i in block_i.items():
                                code_list[tuple([PDG])]=[p_i.PDG,p_i.value]
                        elif type(block_i) is matrix:
                            code_lenth=2
                            for index,element in block_i.element_list.items():
                                code_list[index]=list(index)+[element]
                    else:
                        code_list={}
                        code_lenth=0
                    #print(semanteme[1],code_list,'-'*5)
                else:
                    line_code=tuple(semanteme[:code_lenth])
                    if line_code in code_list.keys():
                        inp.write('  '.join([str(i) for i in code_list[line_code]+semanteme[code_lenth+1:]])+'\n')
                        continue
            inp.write(line)
        inp.close()
        # run SPheno
        #subprocess.Popen('./bin/SPhenoNInvSeesaw SPheno.in',cwd=self.package_dir,shell=True,)

        # run=subprocess.Popen(self.command,cwd=self.package_dir,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        # run.wait()
        # print(run.communicate())
        # if (run.returncode):
        #     ColorPrint(0,33,'',run.communicate()[0])
        #     Error(run.communicate()[1])
        # else:

        r=ReadFiles(self.spectr_dir)
        print(r.MINPAR,r.LAMN)