
# Workflow

## SARAH

官网

[https://sarah.hepforge.org/](https://sarah.hepforge.org/)

说明书

[https://sarah.hepforge.org/sarah_in_a_nutshell.pdf](https://sarah.hepforge.org/sarah_in_a_nutshell.pdf)

### 生成文件

SPheno源代码生成

`MakeSPheno[];`

MicrOmegas源代码生成

`MakeCHep[];`

生成文件路径

`$path/SARAH/Output/$MODEL/EWSB/SPheno/`

`$path/SARAH/Output/$MODEL/EWSB/CHep/`



## SPheno

官网

[https://spheno.hepforge.org/](https://spheno.hepforge.org/)

准备模型文件

用Sarah准备模型文件，下面表示为 $MODEL

NMSSM模型的生成文件：

[NMSSM.zip](file/NMSSM.zip)

```Bash
tar -zxvf SPheno-X.Y.Z.tar.gz
cd SPheno-X.Y.Z
mkdir $MODEL
cp -r $path/SARAH/Output/$MODEL/EWSB/SPheno/* $MODEL/

```


编译

Makefile中修改编译器：F90=gfortran ，或者在下文make语句后加上此句进行参数赋值。

Linux系统下Spheno提供的makefile语句有错误，不能正确地给linker赋值。因此：
增加ar参数：在./src/makefile中，在第8行之后加入 linker = -crUu（ -cr 也可以）

可选：./NMSSM/makefile中，将ar后的参数改为-crUu，可减少warning，见

[https://bugzilla.redhat.com/show_bug.cgi?id=1155273](https://bugzilla.redhat.com/show_bug.cgi?id=1155273)

Mac系统下 将./src/Makefile 删除或附加任意后缀（如Makefile.11），再将./src/Makefile.mac后缀删除即可

```Bash
make Model=$MODEL # F90=gfortran
```


将创建一个新的二进制文件`bin/SPheno$MODEL`

报错：（SARAH4.14.5出现）

22400 | Write(92,"(e16.8)",advancd="No") BR_tWb/gTFu(3)
           |                                                                          1
Error: Function 'gtfu' at (1) has no IMPLICIT type

方案：改用SARAH4.14.3版本

运行

```Bash
./bin/SPheno$MODEL $MODEL/Input_Files/LesHouches.in.$MODEL
```


micromegas可以读取SPheno的输出文件作为输入文件，在运行SPheno时候需要打开开关

```Bash
Block SPhenoInput # SPheno specific input
...
50 0 # Majorana phases : use only positive masses
```


## MicrOmegas

官网

[https://lapth.cnrs.fr/micromegas/](https://lapth.cnrs.fr/micromegas/)

SARAH生成模型文件

[CHep.zip](file/CHep.zip)

```Bash
cd $PATH/MICROMEGAS
./newProject $MODEL
cd $MODEL
cp -r $PATH/SARAH/Output/$MODEL/EWSB/CHep/∗ work/models
```


编译

```Bash
cd $PATH/MICROMEGAS
make
cd $MODEL
mv work/models/CalcOmega_with_DDetection_MOv5.cpp . 
# 注意主程序名后缀**_MOv5**代表MicrOmegas的版本，可在备用主程序中根据需要选择
make main=CalcOmega_with_DDetection_MOv5.cpp
```


将创建一个新的二进制文件`CalcOmega_with_DDetection_MOv5`。

运行

将SPheno的输出文件与`CalcOmega_with_DDetection_MOv5`放在同一路径下：

```Bash
$ cp $PATH/SPHENO/SPheno.spc.$MODEL .
$ ./CalcOmega_with_DDetection_MOv5
```




