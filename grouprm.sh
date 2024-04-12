#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Fri 26 Feb 2021 10:32:41 AM CST
#########################################################################
#!/bin/bash
#echo $1
#echo $2
prefix=${1%-*}
begin=${1#*-}
end=${2#*-}
if [ $# == 1 ] ; then
    end=$begin
fi
echo $begin
echo $end
for id in $(seq $begin $end)
do
    file="${prefix}-${id}"
    #echo $file
    if [ -h $file ]; then
        echo "rm ${file} and models"
        result=`rm -rf $file/model-*`
        result=`rm -rf $file`
    fi
    if [ -d $file ]; then
        echo "rm ${file}"
        #result=`rm -rf $file/model-*`
        result=`mv $file ~/.delete`
    fi
done
