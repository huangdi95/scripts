#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Mon 11 Jan 2021 09:08:15 PM CST
#########################################################################
#!/lustre/S/huangdi/anaconda3/bin/python
import os
process = os.popen('slurm-gpu-queue')
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

mat = "{:10}\t{:1}"

used_gpu = {}
for item in output.split('\n')[1:]:
    if len(item.split()) < 10:
        continue
    user = item.split()[USER]
    node = item.split()[NODE]
    qos = item.split()[QOS]
    tres_per_n = item.split()[TRES_PER_N]
    if user not in used_gpu:
        used_gpu.update({user: 0})
    used_gpu[user] += int(tres_per_n.split(':')[-1]) * int(node)

sorted_dict = sorted(used_gpu.items(),key=lambda x:x[1],reverse=True)
total = 0
for k, v in sorted_dict:
    print(mat.format(k, v))
    total += v
print(mat.format('total', total))
