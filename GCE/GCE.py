#! /usr/bin/env python3
import subprocess,os,sys,shutil

def chisq_GCE(spectr):
    workdir=os.path.dirname(__file__)
    print(workdir)
    order=['./main',os.path.join(spectr)]
    subprocess.Popen(order,cwd=workdir,stdout=subprocess.PIPE).wait()

    run=subprocess.Popen(['./testCovar.py','./GCE_out.txt'],stdout=subprocess.PIPE,cwd=workdir)
    run.wait()
    #print(run)
    #print(run.stdout.read())
    return float(run.stdout.read())

if __name__=='__main__':
    x2=chisq_GCE(sys.argv[1])
    print(float(x2))
    print(x2)
