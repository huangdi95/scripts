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

mat = "{:10}\t{:1}\t{:1}"

used_gpu = {}
for item in output.split('\n')[1:]:
    if len(item.split()) < 10:
        continue
    print(item.split())
    user = item.split()[USER]
    node = item.split()[NODE]
    qos = item.split()[QOS]
    reason = item.split()[-1]
#    tres_per_n = item.split()[TRES_PER_N]
    tres_per_n = item.split()[-3]
    if user not in used_gpu:
        used_gpu.update({user: [0, 0]})
    if reason == 'None':
        used_gpu[user][0] += int(tres_per_n.split(':')[-1]) * int(node)
    else:
        used_gpu[user][1] += int(tres_per_n.split(':')[-1]) * int(node)

sorted_dict = sorted(used_gpu.items(),key=lambda x:x[1],reverse=True)
total = [0, 0]
print(mat.format('USER', 'using', 'pending'))
for k, v in sorted_dict:
    print(mat.format(k, v[0], v[1]))
    total[0] += v[0]
    total[1] += v[1]
print(mat.format('total', total[0], total[1]))
