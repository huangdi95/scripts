#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Fri 26 Feb 2021 10:32:41 AM CST
#########################################################################
#!/bin/bash
#begin=${1%-*}
#end=${1#*-}
echo $1
echo $2
for id in $(seq $1 $2)
do
result=`scancel $id`
done
