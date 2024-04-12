#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Mon 11 Jan 2021 09:08:15 PM CST
#########################################################################
#!/lustre/S/huangdi/anaconda3/bin/python
import os
process = os.popen('slurm-cpu-info')
output = process.read()
process.close()
flag = False

PARTITION      = 0
NODELIST       = 1
STATE          = 2
CPU_LOAD       = 3
SOCKET         = 4
CPUS           = 5
FREE_MEM       = 6
MEMORY         = 7
AVAIL_FEATURES = 8

mat = "{:10}\t{:10}\t{:1}"
print(mat.format('partition', 'name', 'remain'))
for item in output.strip().split('\n')[1:]:
    item = item.split()
    partition = item[PARTITION]
    nodelist = item[NODELIST]
    cpus = item[CPUS]
    #print(cpus)
    A, I, O, T = cpus.split('/')
    remain = I
    #if 'drain' in item or 'down' in item or 'drng' in item:
    #    flag = True
    #if 'cpu-fat' in item:
    #    partition = 'cpu-fat'
    #elif 'cpu' in item:
    #    partition = 'cpu'
    #elif 'cpu-' in item or 'gpu-' in item:
    #    name = item
    #elif 'gpu:' in item and 'IDX:' not in item:
    #    total = int(item.split(':')[1][0])
    #elif 'IDX:' in item:
    #    used = int(item.split(':')[2][0].split('(')[0])
    #    remain = total - used
    #    if remain == 0:
    #        flag = True
    #elif 'IB,' in item:
    #    features = item.split(',')[3]
    #    if flag:
    #        flag = False
    #        continue
    if int(remain) > 0:
        print(mat.format(partition, nodelist, remain))
