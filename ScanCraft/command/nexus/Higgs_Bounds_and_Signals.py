#! /usr/bin/env python3
import os,shutil,subprocess
try:
    from .GetPackageDir import GetPackageDir
    from .color_print import ColorPrint,UseStyle,Error
    from .read.readline import ReadLine
    from ..format.data_container import capsule
except:
    pass

class HiggsBounds():
    def __init__(self,
                    target_dir,
                    package_dir=None,
                    model='NMSSM',
                    mode='',
                    silent=False
                ):
        if package_dir==None:
            package_dir=GetPackageDir('HiggsBounds',silent=silent)
        elif not os.path.exists(package_dir):
            Error('directory --%s-- not found, please check its path'%package_dir)
        
        if model=='NMSSM':
            n_neutral=5
            n_charged=1
        elif model=='MSSM':
            n_neutral=3
            n_charged=1

        if mode in ['SARAH']:
            self.package_dir=package_dir
            self.target_dir=target_dir
            main_routine=os.path.join(package_dir,'./HiggsBounds')
            if os.path.exists(main_routine):
                if not silent:print('HiggsBounds\' main routine specified:\n->',os.path.join(package_dir,main_routine))
            else:
                Error('HiggsSingals\' main routine --%s-- not found, please check its path'%main_routine)

            self.command=' '.join([main_routine,'LandH effC',str(n_neutral),str(n_charged),'./'])
            self.output_dir=os.path.join(target_dir,'HiggsBounds_results.dat')
        else:
            Error('mode not recognised, contact He Yangle.')

    def RunSARAH(self):
        run=subprocess.Popen(self.command,cwd=self.target_dir,shell=True,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        run.wait()
        if (run.returncode):
            ColorPrint(0,33,'',run.communicate()[0])
            Error(run.communicate()[1])
        result=capsule()
        result.HBresult_string=open(self.output_dir).readlines()[-1]
        semanteme=ReadLine(result.output_line)        
        result.HBresult=semanteme[7]
        result.obsratio=semanteme[9]
        result.channel=semanteme[8]
        return result
    
    def Record(self,number:int,record_dir=None,digit_width:int=8):
        if record_dir==None:
            record_dir=os.path.join(self.target_dir,'record')
        suffix=f'.{number:0>{digit_width}}'
        documents={'HBresult':os.path.join(record_dir,'HBresults.dat'+suffix)}
        shutil.copy(self.output_dir,documents['HBresult'])
        return documents

        
class HiggsSignals():
    def __init__(self,
                    target_dir,
                    package_dir=None,
                    model='NMSSM',
                    mode=''):
        if package_dir==None:
            package_dir=GetPackageDir('HiggsSignals')
        elif not os.path.exists(package_dir):
            Error('directory --%s-- not found, please check its path'%package_dir)
        
        if model=='NMSSM':
            n_neutral=5
            n_charged=1
        elif model=='MSSM':
            n_neutral=3
            n_charged=1

        if mode in ['SARAH']:
            self.package_dir=package_dir
            self.target_dir=target_dir
            main_routine='./HiggsSignals'
            if os.path.exists(os.path.join(package_dir,main_routine)):
                print('HiggsSingals\' main routine specified:\n->',os.path.join(package_dir,main_routine))
            else:
                Error('HiggsSingals\' main routine --%s-- not found, please check its path'%main_routine)

            self.command=' '.join([main_routine,'latestresults peak 2 effC',str(n_neutral),str(n_charged),target_dir])
            self.output_dir=os.path.join(target_dir,'HiggsSignals_results.dat')
        else:
            Error('mode not recognised, contact He Yangle.')

    def RunSARAH(self):
        run=subprocess.Popen(self.command,cwd=self.package_dir,shell=True,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        run.wait()
        if (run.returncode):
            ColorPrint(0,33,'',run.communicate()[0])
            Error(run.communicate()[1])
        result=data_list()
        result.output_line=open(self.output_dir).readlines()[-1]
        semanteme=ReadLine(result.output_line)
        result.Pvalue=semanteme[-1]
        return result

        
# class Higgs_BaS():
#     def __init__(self,
#                     target_dir,
#                     package_dir=None,):
#         if package_dir==None:
#             package_dir=GetDir('HiggsBounds')
#         elif not os.path.exists(package_dir):
#             Error('directory --%s-- not found, please check its path'%package_dir)