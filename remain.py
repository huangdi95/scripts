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
QOS         = 6
NODE        = 7
TASK        = 8
CPUS        = 9
TRES_PER_N  = 10
NODELIST    = 11

mat = "{:10}\t{:1}"

max_gpu = {
    'gpu-trial'   : 32, 
    'gpu-debug'   : 32, 
    'gpu-short'   : 32, 
    'gpu-normal'  : 32, 
    'gpu-long'    : 16,
    'gpu-longlong': 8}
for item in output.split('\n')[1:]:
    if len(item.split()) < 10:
        continue
    qos        = item.split()[QOS]
    if qos == 'gpu-longlo':
        qos = 'gpu-longlong'
    tres_per_n = item.split()[TRES_PER_N]
    max_gpu[qos] -= int(tres_per_n.split(':')[-1])

print(mat.format('QOS', 'remain'))
for qos in max_gpu:
    print(mat.format(qos, max_gpu[qos]))
