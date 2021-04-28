#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Fri 26 Feb 2021 10:32:41 AM CST
#########################################################################
#!/bin/bash
result=`sbatch $1`
echo $result
arr=($result)
file="ret-${arr[-1]}.err"
sleep 1.0s
while [ ! -f "$file" ]
do
    sleep 0.5s
done
tail -f $file
