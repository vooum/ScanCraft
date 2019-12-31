import os, shutil

def batchRenameFile(srcDir, destDir):  # srcDir 为源文件夹的绝对路径；destDir 为目标文件夹的绝对路径
    i = 1; b = 1;a = 0
    subDirList = os.listdir(srcDir) #读取路径
    for subDir in subDirList:       #循环开始
        a = 0;
        while subDir[a] != '_':
            a += 1                #找到下划线位置，对'inp0_21'时a为4
        b = a-1
        while subDir[b:a].isdigit() :#找到数字的位置为[b+1:a],记得加冒号嗷嗷嗷
            b -= 1
        b += 1                    #[b:a]好看
        fileList = os.path.join(srcDir,subDir)    # 须绝对路径
        print(fileList)
        if not os.path.isdir(destDir+'/data'):#目标文件夹/data/data0如果不存在就创建文件夹。存在则else自动pass了
            print('准备创建data')
            os.mkdir(destDir+'/data')
        if not os.path.isdir(destDir+'/data'+'/data'+subDir[b:a]):
            os.mkdir(destDir+'/data'+'/data'+subDir[b:a])
            print('已创建二级目录')
        shutil.copy(fileList, destDir+'/data'+'/data'+subDir[b:a]+'/'+subDir[0:b]+'.dat.'+subDir[a+1:])
        # 目标文件夹/data/data0/inp.dat.21
        i = i+1
srcDir = r'C:\Users\Administrator\Desktop\新建文件夹 (3)\Results\spectrs'#【源文件夹】
destDir = r'C:\Users\Administrator\Desktop\目标文件夹3'#【目标文件夹】
batchRenameFile(srcDir, destDir)
print('批量移动并命名完成')
