#!/usr/bin/env python3

class package(object):
    def __init__(self
                ,package_name           #程序包的名字
                ,package_dir            #程序包所在的目录
                ,run_dir                #可执行文件的目录
                ,main_routine           #运行命令
                ,data_dir               #保留数据的目录
                ,model_dir              #模型目录
                ,input_dir              #输入文件所在的目录
                ,input_file             #输入文件
                ,output_dir             #输出文件的目录
                ,record_dir             #保留输出文件的目录
                ,out_file               #输出文件
                ):
        self.package_dir=package_dir
        self.run_dir=run_dir




    def Run(self):
        pass


    def Record(self):
        pass

