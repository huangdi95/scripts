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
flag = False

history = []
print('Finished')
with open('/lustre/S/huangdi/scripts/log.task_id',mode='r') as f:
    for l in f.readlines():
        history.append(l.replace('\n', ''))

current = []
f = open('/lustre/S/huangdi/scripts/log.task_id',mode='w')
for item in output.split('\n')[1:]:
    if len(item.split()) < 10:
        continue
    if item.split()[3] == 'debug':
        continue
    task_id = item.split()[0]
    current.append(task_id)
    f.write(task_id + '\n')
f.close()

for task_id in history:
    if task_id not in current:
        print(task_id)
