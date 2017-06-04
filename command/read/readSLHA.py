#! /usr/bin/env python3

from .readline import commented_out,ReadLine
class ReadBlock():
    scalar_block=dict.fromkeys(['MINPAR'],'Scalar')
    matrix_block=dict.fromkeys(['LAMN'],'Matrix')
    block_types=dict(list(scalar_block.items())+list(matrix_block.items()))
    def Scalar(line):
        if commented_out(line):
            return {}
        else:
            semanteme=ReadLine(line)
            try:
                return {int(semanteme[0]):semanteme[1]}
            except IndexError:
                return {}
    def Matrix(line):
        #print(line)
        if commented_out(line):
            print(2)#return {1:1}
        else:
            semanteme=ReadLine(line)
            try:
                return {tuple([int(semanteme[0]),int(semanteme[1])]):semanteme[2]}
            except IndexError:
                return {}



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



class empty():
    pass
class readSLHA():
    def __init__(self,sample=None):
        if sample==None:
            self.sample=empty()
        else:
            self.sample=sample
def ReadFiles(*files):
    sample=empty()
    for file_i in files:
        ReadSLHAFile(sample,file_i)
    return sample

if __name__=='__main__':
    print(ReadBlock.block_types)