#!/bin/bash
c=`find ./ -maxdepth 1 -name "*.py" -type f`
echo $c
n=` echo $c | wc -w`
#echo $n
if [ $n -ne 1 ]; then
 echo $n 'files'
 for  word in $c;
 do
  echo $word
 done
#exit()
else
 echo y | nohup $c > screen 2>&1 &
fi
