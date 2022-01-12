#########################################################################
# Author: Huang Di
# Mail: hd232508@163.com
# Created Time: Mon 11 Jan 2021 09:08:15 PM CST
#########################################################################
#!/lustre/S/huangdi/anaconda3/bin/python
import os
import sys
process = os.popen('squeue -O JobID,Partition,NodeList,tres-per-node,EndTime,Account')
output = process.read()
process.close()

JOBID       = 0
PARTITION   = 1
NODE        = 2
TRES_PER_N  = 3
ENDTIME     = 4
USER        = 5

mat = "{:8}\t{:8}\t{:8}\t{:1}"

end_list = []
max_gpu = {
    'gpu-trial'   : 32, 
    'gpu-debug'   : 32, 
    'gpu-short'   : 32, 
    'gpu-normal'  : 32, 
    'gpu-long'    : 16,
    'gpu-longlong': 8}
for item in output.split('\n')[1:]:
    if len(item.split()) < 6:
        continue
    partition = item.split()[PARTITION]
    node      = item.split()[NODE]
    t_p_n     = item.split()[TRES_PER_N]
    end_time  = item.split()[ENDTIME]
    user      = item.split()[USER]
    if t_p_n.split(':')[-1] == 'N/A':
        continue
    if int(t_p_n.split(':')[-1]) < 4:
        continue
    if sys.argv[1] == 'me' and user != 'huangdi':
        continue 
    end_list.append((partition, node, t_p_n, end_time))
end_list.sort(key = lambda x: x[3], reverse=True)

print(mat.format('Partition', 'Node', 'Tres_per_node', 'EndTime'))
for partition, node, t_p_n, end_time in end_list:
    print(mat.format(partition, node, t_p_n, end_time))
