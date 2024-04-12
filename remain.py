#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Mon 11 Jan 2021 09:08:15 PM CST
#########################################################################
#!/lustre/S/huangdi/anaconda3/bin/python
import os
process = os.popen('slurm-gpu-queue --me')
output = process.read()
process.close()


JOBID       = 0
USER        = 1
PARTITION   = 2
NAME        = 3
STATE       = 4
TIME        = 5
TIME_LIMIT  = 6
QOS         = 7
FEATURES    = 8
NODE        = 9
TASK        = 10
CPUS        = 11
TRES_PER_N  = 12
NODELIST    = 13
REASON      = 14

mat = "{:10}\t{:1}\t{:9}"

remain_gpu = {
    'gpu-trial'   : 32, 
    'gpu-debug'   : 32, 
    'gpu-short'   : 32, 
    'gpu-normal'  : 32, 
    'gpu-long'    : 16,
    'gpu-longlong': 8}
remain_task = {
    'gpu-trial'   : 8, 
    'gpu-debug'   : 8, 
    'gpu-short'   : 8, 
    'gpu-normal'  : 8, 
    'gpu-long'    : 4,
    'gpu-longlong': 2}
for item in output.split('\n')[1:]:
    if len(item.split()) < 10:
        continue
    qos        = item.split()[QOS]
    if qos == 'gpu-longlo':
        qos = 'gpu-longlong'
    tres_per_n = item.split()[TRES_PER_N]
    remain_gpu[qos] -= int(tres_per_n.split(':')[-1])
    remain_task[qos] -= 1

print(mat.format('QOS', 'remain_gpus', 'remain_tasks'))
for qos in remain_gpu:
    print(mat.format(qos, remain_gpu[qos], remain_task[qos]))
