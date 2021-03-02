#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Mon 11 Jan 2021 09:08:15 PM CST
#########################################################################
#!/lustre/S/huangdi/anaconda3/bin/python
import os
process = os.popen('slurm-gpu-info')
output = process.read()
process.close()
flag = False

mat = "{:10}\t{:10}\t{:1}"
print(mat.format('partition', 'name', 'remain'))
for item in output.split():
    if 'drain' in item or 'down' in item or 'drng' in item:
        flag = True
    if 'nv-gpu-hw' in item:
        partition = 'nv-gpu-hw'
    elif 'nv-gpu' in item:
        partition = 'nv-gpu'
    elif 'compute-' in item or 'gpu-' in item:
        name = item
    elif 'S:0' in item:
        total = int(item.split(':')[1][0])
    elif 'IDX:' in item:
        used = int(item.split(':')[2][0])
        remain = total - used
        if remain == 0 or flag:
            flag = False
            continue
        mat = "{:10}\t{:10}\t{:1}"
        print(mat.format(partition, name, remain))
