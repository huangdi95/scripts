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

mat = "{:10}\t{:10}\t{:10}\t{:1}"

flag = False

history = []
with open('/lustre/S/huangdi/scripts/log.task_id',mode='r') as f:
    for l in f.readlines():
        task = tuple(l.replace('\n', '').split())
        history.append(task)

current = []
f = open('/lustre/S/huangdi/scripts/log.task_id',mode='w')
for item in output.split('\n')[1:]:
    if len(item.split()) < 10:
        continue
    if item.split()[NAME] == 'debug':
        continue
    task_id  = item.split()[JOBID]
    name     = item.split()[NAME]
    qos      = item.split()[QOS]
    nodelist = item.split()[NODELIST]
    task = (task_id, name, qos, nodelist)
    current.append(task)
    f.write(' '.join(task) + '\n')
f.close()

print(mat.format('FinishedID', 'NAME', 'QOS', 'NODELIST'))
for task in history:
    if task not in current:
        print(mat.format(task[0], task[1], task[2], task[3]))

print(mat.format('NewID', 'NAME', 'QOS', 'NODELIST'))
for task in current:
    if task not in history:
        print(mat.format(task[0], task[1], task[2], task[3]))
