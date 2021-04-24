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

f = open('/lustre/S/huangdi/scripts/log.task_id',mode='w')
for item in output.split('\n')[1:]:
    if len(item.split()) < 10:
        continue
    task_id = item.split()[0]
    if task_id not in history:
        print(task_id)
    f.write(task_id + '\n')
f.close()
