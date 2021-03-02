#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Fri 26 Feb 2021 10:32:41 AM CST
#########################################################################
#!/bin/bash
result=`sbatch $1`
echo $result
arr=($result)
sleep 1.5s
tail -f "ret-${arr[-1]}.err"
