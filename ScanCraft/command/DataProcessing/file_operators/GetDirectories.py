import os,re

'''2021/08/06
收集有特定格式的文件夹到一个list里，用于读取多个文件夹里的数据文件，类似glob
推荐用glob
'''
def GetNumber(text):
    return int(re.findall(r'\d+',text)[-1])

def GetDirectories(path='./',keyword=None,numbered=False):
    '''collect all folders containing keyword(s) at given path,
        then return their abspath in a list.
    If numbered is False, folders without number in name will be included,
    if numbered is True, folders without number in name will be discard.
    '''
    if keyword is None: keyword='mcmc'
    file_list=[]
    candidate={}
    total=0

    with os.scandir(path) as entries:
        for entry in entries:
            if (keyword in entry.name) and entry.is_dir():
                try:
                    candidate.update( {GetNumber(entry.name):entry} )
                except IndexError: # no number in filename
                    if numbered:
                        continue
                    else:
                        candidate.update({-1-total:entry})
                else:
                    total+=1
    if total != len( candidate.keys() ):
        print(f'{total} folder get index, but {len(candidate)} folder recorded in the list.
        Maybe one number was allocated to multiple folders.')
        exit('number conflict')
    file_list=[os.path.abspath(candidate[i]) for i in sorted(candidate.keys())]
    return file_list