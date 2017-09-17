#! /usr/bin/env python3
import os,shutil,subprocess,copy
try:
    from .operations.GetDir import GetDir
    from .data_type import scalar,matrix
    from .read.readSLHA import ReadSLHAFile

    from .read.readSLHA import ReadBlock
    from .read.readline import commented_out,ReadLine
    from .data_type import data_list

    from .color_print import ColorPrint,UseStyle,Error
except:
    raise
    pass


def output_information_of_NMSSMTools(text):
    semanteme=ReadLine(text.lines[text.i])
    if semanteme[1].upper()!='SPINFO':
        Error('wrong when entering Read_SPINFO')
    info={}
    for i in range(1,5):
        info[i]=[]
    while True:
        try:
            line=text.NextLine()
        except IndexError:
            break
        else:
            if commented_out(line):
                continue
            semanteme=ReadLine(line)
            if str(semanteme[0]).upper()=='BLOCK':
                break

            info_number=int(semanteme[0])
            if info_number in info.keys():
                info[info_number].append(semanteme[1])
                # print(info_number,info[info_number])
            else:
                Error(line)
    return info

def Annihilation_in_omegas(text):
    anni={}
    while True:
        try:
            line=text.NextLine()
        except IndexError:
            break
        else:
            if commented_out(line):
                continue
            semanteme=ReadLine(line)
            try:
                number=semanteme[0]
            except IndexError:
                continue
            else:
                if str(number).upper()=='BLOCK':
                    break
                elif int(number)==0:
                    anni.update({(0,0):semanteme[1]})
                else:
                    nf=int(semanteme[2])
                    tuple_f=tuple([int(i) for i in semanteme[3:3+nf]])
                    anni.update({tuple_f:semanteme[1]})
    return anni

def read_ABUNDANCE_in_omegas(text):
    DM={}#{'contribution_vSigma':[],'contribution_Omega':[]}
    while True:
        try:
            line=text.NextLine()
        except IndexError:
            break
        else:
            if commented_out(line):
                continue
            semanteme=ReadLine(line)
            try:
                number=semanteme[0]
            except IndexError:
                continue
            else:
                if str(number).upper()=='BLOCK':
                    break
                # elif int(number)==6:
                #     DM['contribution_vSigma'][tuple(semanteme[4:6])]=semanteme[6]
                # elif int(number)==7:
                #     DM['contribution_Omega'][tuple(semanteme[4:6])]=semanteme[6]
                elif int(number)<5:
                    DM[semanteme[0]]=semanteme[1]

class new_ReadBlock(ReadBlock):
    SPINFO=output_information_of_NMSSMTools
    ANNIHILATION=Annihilation_in_omegas
    ABUNDANCE=read_ABUNDANCE_in_omegas
def ReadNMSSMToolsSpectr(spectr_dir,ignore=[]):
    result=data_list()
    ReadSLHAFile(spectr_dir,result,block_format=new_ReadBlock)
    omega_dir=spectr_dir.replace('spectr','omega')
    try:
        ReadSLHAFile(omega_dir,result)
    except:
        pass
    result.ERROR=bool(result.SPINFO[4])
    result.constraints=[]
    for constraint in result.SPINFO[3]:
        for const in ignore:
            if const in constraint:
                break
        else:
            result.constraints.append(constraint)
    return result

class NMSSMTools():
    def __init__(self,
                    package_dir=None,
                    data_dir='mcmc/',
                    in_model='inp.dat',
                    output_file='spectr.dat'):
        if package_dir==None:
            package_dir=GetDir('NMSSMTools')
        elif not os.path.exists(package_dir):
            Error('directory --%s-- not found, please check its path'%package_dir)

        self.package_dir=package_dir
        self.inp_model_lines=open(os.path.join(data_dir,in_model),'r').readlines()
        self.inp_file='inp.dat'#-----------
        self.inp_dir=os.path.join(package_dir,self.inp_file)
        self.output_file=output_file
        self.output_dir=os.path.join(package_dir,self.output_file)
        self.output_omega_file=self.output_file.replace('spectr','omega')
        self.output_omega_dir=self.output_dir.replace('spectr','omega')
        self.record_dir=os.path.join(data_dir,'./record/')
        main_routine='./run'
        self.command=' '.join([main_routine,self.inp_file])

        if os.path.exists(self.record_dir):
            if input(UseStyle('delete folder record? (y/n) \n',mode=1,fore=34)).upper() in ['Y','YES','']:
                shutil.rmtree(self.record_dir)
            else:
                exit('folder record/ is not deleted')
        os.mkdir(self.record_dir)
    
    def Run(self,point,ignore=[]):
        # write input file for SPheno
        inp=open(self.inp_dir,'w')
        for line in self.inp_model_lines:
            if not commented_out(line):
                semanteme=ReadLine(line)
                if str(semanteme[0]).upper()=='BLOCK':
                    code_list={}
                    code_lenth=0
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
                    #print(semanteme[1],code_list,'-'*5)
                else:
                    line_code=tuple(semanteme[:code_lenth])
                    if line_code in code_list.keys():
                        inp.write('\t'+'\t'.join([str(i) for i in code_list[line_code]+semanteme[code_lenth+1:]])+'\n')
                        continue
            inp.write(line)
        inp.close()
        # ------------run
        try:
            os.remove(self.output_dir)
            os.remove(self.output_omega_dir)
        except:
            pass

        run=subprocess.Popen(self.command,cwd=self.package_dir,shell=True,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        run.wait()
        if (run.returncode):
            ColorPrint(0,33,'',run.communicate()[0])
            Error(run.communicate()[1])
        
        result=ReadNMSSMToolsSpectr(self.output_dir,ignore=ignore)

        return result
        
    def Record(self,number):
        shutil.copy(self.inp_dir,os.path.join(self.record_dir,self.inp_file+'.'+str(int(number))))
        shutil.copy(self.output_dir,os.path.join(self.record_dir,self.output_file+'.'+str(int(number))))
        try:
            shutil.copy(self.output_omega_dir,os.path.join(self.record_dir,self.output_omega_file+'.'+str(int(number))))
        except:
            pass