#! /usr/bin/env python3

try:
    from ..data_type import data_list
    from .readline import commented_out,ReadLine
except:
    if __name__=='__main__':
        pass
    else:
        raise

scalar_groups={
    'SUSY_input':   ['MINPAR','EXTPAR'],
    'additional':   ['NMSSMRUN','MSOFT'],
    'output'    :   ['MASS','SPhenoLowEnergy','FlavorKitQFV']
}
scalar_groups['input']=[ i+'IN' for i in scalar_groups['additional'] ]


matrix_groups={
    'Mass'      :   ['MSD2','MSE2','MSL2','MSQ2','MSU2'],
    'Triliner'  :   ['TD','TE','TU'],
    'SeeSaw'    :   ['LAMN',],
    'output'    :   ['YE','YU','YD']
}
matrix_groups['input']=[ i+'IN' for j in ['Mass','Triliner','SeeSaw'] for i in matrix_groups[j] ]


scalar_list=[ i.upper() for j in scalar_groups.values()  for i in j ]
matrix_list=[ i.upper() for j in matrix_groups.values()  for i in j ]

class ReadBlock():
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

    def HIGGSBOUNDSRESULTS(line):
        if not commented_out(line):
            pass
            


def PassLine(*args):
    return# {}

def ReadSLHAFile(sample,file_name):
    read=PassLine
    sample.DECAY={}
    for line in open(file_name,'r').readlines():
        semanteme=ReadLine(line)
        #print(semanteme)
        try:
            if str(semanteme[0]).upper()=='BLOCK':
                bi=semanteme[1].upper()
                setattr(sample,bi,{})
                data_dict=getattr(sample,bi)
                if hasattr(ReadBlock,bi):
                    read=getattr(ReadBlock,bi)
                elif bi in ReadBlock.block_types.keys():
                    #print(ReadBlock.block_types)###
                    read=getattr(ReadBlock,ReadBlock.block_types[bi])
                else:
                    read=PassLine
            elif str(semanteme[0]).upper()=='DECAY':
                di=int(semanteme[1])
                width_i=semanteme[2]
                data_dict=sample.DECAY[di]={}
                read=PassLine
            else:
                try:
                    data_dict.update(read(line))
                except:
                    pass
        except:
            continue


def ReadFiles(*files):
    sample=data_list()
    for file_i in files:
        ReadSLHAFile(sample,file_i)
    return sample

if __name__=='__main__':
    #print(ReadBlock.block_types)
    print(scalar_list)
    print(matrix_list)