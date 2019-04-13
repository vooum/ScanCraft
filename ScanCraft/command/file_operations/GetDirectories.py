import os,re

def GetDirectories(path='./',keyword=None,numbered=None):
    if keyword is None: keyword='mcmc'
    if numbered is None: numbered=False
    file_list=[]
    candidate={}
    total=0
    for document in os.listdir(path):
        if (keyword in document) and os.path.isdir(os.path.join(path,document)):
            try:
                number=int(re.findall(r'\d+',document)[-1])
            except IndexError:
                if not numbered:
                    candidate.update({-1-total:document})
                    total+=1
            else:
                candidate.update({number:document})
                total +=1
    # for i in sorted(candidate.keys()):
        # file_list.append(os.path.join(os.getcwd(),path,document))
    if total !=len(candidate.keys()):
        print(len(candidate),total)
        exit('number conflict')
    # file_list=[os.path.join(os.getcwd(),path,candidate[i]) for i in  sorted(candidate.keys())]
    file_list=[os.path.abspath(os.path.join(path,candidate[i])) for i in sorted(candidate.keys())]
    return file_list