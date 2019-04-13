#! /usr/bin/env python3

# try:
# from ..data_type import data_list
from .readline import commented_out,ReadLine
from .special_blocks import special_blocks
from ..format.data_container import capsule
from .SLHA_string import SLHA_string
# except:
#     if __name__=='__main__':
#         pass
#     else:
#         raise

scalar_groups={
    'SUSY_input':   ['MINPAR','EXTPAR'],
    'additional':   ['NMSSMRUN','MSOFT'],
    'output'    :   ['MASS','SPhenoLowEnergy','FlavorKitQFV','LOWEN','LHCFIT','FINETUNING'],
    'omega'     :   ['ABUNDANCE','LSP','NDMCROSSSECT','INDIRECT_CHISQUARES']
}
scalar_groups['input']=[ i+'IN' for i in scalar_groups['additional'] ]# for Spheno


matrix_groups={
    'Mass'      :   ['MSD2','MSE2','MSL2','MSQ2','MSU2'],
    'Mix'       :   ['NMHMIX','NMAMIX','STOPMIX','NMNMIX'],
    'Triliner'  :   ['TD','TE','TU'],
    'SeeSaw'    :   ['MUX','MV2','MX2','YV','TV','BMUX','LAMN','TLAMN'],
    'output'    :   ['YE','YU','YD',
                     'HiggsLHC13','HiggsLHC14','REDCOUP']
}
matrix_groups['input']=[ i+'IN' for j in ['Mass','Triliner','SeeSaw'] for i in matrix_groups[j] ]# for Spheno


scalar_list=[ i.upper() for j in scalar_groups.values()  for i in j ]
matrix_list=[ i.upper() for j in matrix_groups.values()  for i in j ]

class ReadBlock(special_blocks):
    scalar_block=dict.fromkeys(scalar_list,'Scalar')
    matrix_block=dict.fromkeys(matrix_list,'Matrix')
    block_types=dict(list(scalar_block.items())+list(matrix_block.items()))
    def Scalar(line):
        if not commented_out(line):
            semanteme=ReadLine(line)
            try:
                return {int(semanteme[0]):semanteme[1]}
            except IndexError:
                return {}
    def Matrix(line):
        #print(line)
        if not commented_out(line):
            semanteme=ReadLine(line)
            try:
                return {tuple([int(semanteme[0]),int(semanteme[1])]):semanteme[2]}
            except IndexError:
                return {}
    def ReadDecay(line):
        if not commented_out(line):
            semanteme=ReadLine(line)
            try:
                nf=int(semanteme[1])# number of final particles
                f=tuple([int(i) for i in semanteme[2:2+nf]])# final particles' PDG tuple
                return {f:semanteme[0]}
            except:
                return {}

    # def HIGGSBOUNDSRESULTS(line):
    #     print(line)
    #     if not commented_out(line):
    #         pass
            
class content():
    def __init__(self,file_name):
        document=open(file_name,'r')
        lines=document.readlines()
        document.close()
        self.lines=[SLHA_string(i) for i in lines]
        self.i=-1
    def NextLine(self):
        self.i+=1
        return self.lines[self.i]

def PassLine(*args):
    return {}

def SetDecay(obj): # be the default value of getattr, to set an attribute to obj
    setattr(obj,'DECAY',{})
    return getattr(obj,'DECAY')


def ReadSLHAFile(file_name,block_format=None):#read information in file_name and store in sample.
    if block_format is None:
        block_format=ReadBlock
    sample=capsule()
    read=PassLine
    text=content(file_name)

    while True:
        try:
            line=text.NextLine()# iterator
        except IndexError:
            break

        semanteme=ReadLine(line)
        #print(semanteme)
        try:
            if str(semanteme[0]).upper()=='BLOCK':
                bi=semanteme[1].upper()
                if not hasattr(sample,bi): setattr(sample,bi,{})
                data_dict=getattr(sample,bi)
                if bi in block_format.block_types.keys():
                    #print(block_format.block_types)###
                    read=getattr(block_format,block_format.block_types[bi])
                else:
                    if hasattr(block_format,bi):
                        data_dict.update(getattr(block_format,bi)(text))
                        text.i-=1
                    read=PassLine
            elif str(semanteme[0]).upper()=='DECAY':
                di=int(semanteme[1])
                DECAY=getattr(sample,'DECAY',SetDecay(sample))
                DECAY[di]={}
                data_dict=DECAY[di]
                data_dict['width']=float(semanteme[2])
                read=block_format.ReadDecay
            else:
                try:
                    data_dict.update(read(line))
                except:
                    pass
        except IndexError:
            pass
    return sample

# def ReadFiles(*files,sample=None):# read information in multiple files and return a data_list object which store information.
#     if sample==None:
#         sample=data_list()
#     for file_i in files:
#         ReadSLHAFile(file_i,sample)
#     return sample

if __name__=='__main__':
    #print(ReadBlock.block_types)
    print(scalar_list)
    print(matrix_list)