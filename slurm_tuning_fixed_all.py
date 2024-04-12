import os
import sys
import time
import numpy as np
from itertools import product
import csv

'''
Need to config:
params_dict: the dict to config the params
slurm_file: the file to submit the job
params_file: the file to config the params
params_indent: the indent of the params in params_file
csv_file: the file to save the results
link_path: the path to create the link of results
'''
slurm_file = './run_IO_modular_fixed_all.slurm'
sh_file = './run_IO_modular_fixed_all.sh'
link_path = './trained_models/tuning_map_fixed_all/'
new_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
csv_file = 'log.tuning_csvs/tuning_fixed_all_' + new_time + '.csv'
os.makedirs(link_path, exist_ok=True)

minimum_qos = 'gpu-normal'
maximum_qos = 'gpu-longlong'

fast_qos = True 
num_gpus = 8
start_idx = 0

params_dict = {}
params_dict.update({'dataset': ["'module_m_s_min_max_10000'", "'module_m_s_min_max_20000'", "'module_m_h'", "'module_m_t'"]})
params_dict.update({'activation': ["'gelu'"]})
params_dict.update({'modular.share': ["True"]})
params_dict.update({'modular.hid_dim': [256]})
#params_dict.update({'modular.hid_dim': [256]})
params_dict.update({'modular.n_layers': [2]})
#params_dict.update({'modular.n_layers': [2]})
params_dict.update({'modular.module_pf_dim': ['hid_dim * 4']})
params_dict.update({'modular.module_heads': ['hid_dim // 64']})
params_dict.update({'modular.repeat_times': [4]})
params_dict.update({'modular.module_dropout': [0.1, 0]})
#params_dict.update({'modular.module_dropout': [0.1]})
# params_dict.update({'modular.communication_dropout': ["module_dropout"]})
# params_dict.update({'modular.enc_dropout': ["module_dropout"]})
params_dict.update({'modular.enc_layers': [4]})
params_dict.update({'batch_size': ['int(128)']})
#params_dict.update({'fixed.communication': ["False", "True"]})
#params_dict.update({'fixed.communication': ["False"]})
# params_dict.update({'fixed.method': ["'attention'", "'dynamic_mask'"]})
#params_dict.update({'fixed.method': ["'dynamic_mask'"]})

#params_dict.update({'transformer.enc_pf_dim': ['enc_hidden', 'enc_hidden * 2']})
#params_dict.update({'transformer.enc_heads': [8]})
#params_dict.update({'transformer.encode_method': ["'first'", "'mean'"]})

#params_dict.update({'transformer.past_emb': [True, False]})
#params_dict.update({'vae.beta_anneal_epoch': [None, 5, 15]})

#params_dict.update({'transformer.enc_pf_dim': [512]})
#params_dict.update({'transformer.enc_layers': [4]})
#params_dict.update({'transformer.dec_layers': [1, 2, 4]})
#params_dict.update({'transformer.dropout': [0., 0.1]})
params_dict.update({'DEBUG': [False]})

block_list = [
    (),
    (),
]

white_list = [
#    (),
#    (),
]

use_white_list = True

#block_dict = {}
#for keys in params_dict:
#    block_dict.update({keys: []})

if fast_qos:
    fast_qos = 'gpu-short'
else:
    fast_qos = None
#slurm_file = './run_IO_vae_condition.slurm'
params_file = './params.py'
params_indent = ' ' * 4
lock_file = params_file + '.lock'

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

def shell(command):
    process = os.popen(command)
    output = process.read()
    process.close()
    return output

def submit():
    feature_list = valid_features()
    #print(feature_list)
    for i, feature in enumerate(feature_list):
        config_feature(feature)
        output = shell('sbatch ' + slurm_file)
        #print(output)
        job_id = output.split()[-1]
        if i == len(feature_list) - 1: # least demanding features
            break
        waiting_time = 0
        failed = False
        state = None
        while state != 'RUNNING':
            state = get_state_status(job_id)
            #print(state)
            time.sleep(0.5)
            waiting_time += 0.5
            if waiting_time >= 60: # waiting for 1 minute
                failed = True
                break
        if not failed:
            break
        shell('scancel ' + job_id) 
        print('scancel ' + job_id)
        
    print(output)
    ret_file = 'rets/ret-' + job_id + '.err'

    while not os.path.exists(ret_file):
        time.sleep(0.5)

    old_time = None
    saved_dir = None
    while True:
        time.sleep(2)
        with open(ret_file, 'r') as f:
            for line in f.readlines():
                if line.startswith('saved to:'):
                    old_time = line.split('/')[-1].split('-')[-1].strip()
                    saved_dir = line.split('/')[-1].strip()
                    saved_dir_all_path = line.strip().split()[-1]
                    break
        if old_time is not None:
            break
    
    if os.path.exists(lock_file):
        os.remove(lock_file)
    
    while True:
        time.sleep(1)
        new_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        if new_time != old_time:
            break
    return job_id, saved_dir, saved_dir_all_path

def config_params(keys, values):
    # lock params.py while configuring
    while os.path.exists(lock_file):
        time.sleep(1)
    os.mknod(lock_file)

    file_data = ""
    class_name = [] # match class params
    keys_visited = [False] * len(keys)

    with open(params_file, "r") as f:
        for line in f:
            if not line.startswith(params_indent * len(class_name)) and line.strip() != '':
                leading_space = len(line) - len(line.lstrip())
                class_name = class_name[:int(leading_space / len(params_indent))]
            if line.strip().startswith('class '):
                class_name.append(line.strip().replace('class ', '').replace('():', ''))
            
            for idx in range(len(keys)):
                key_class = keys[idx].split('.')[:-1]
                key_var = keys[idx].split('.')[-1]
                if key_class != class_name:
                    continue
                #print(key_class)
                #print(class_name)
                if line.strip().startswith(key_var):
                    if keys_visited[idx]:
                        raise Exception('Duplicated key: ' + keys[idx])
                    line = '='.join(line.split('=')[:-1]) + '= ' + str(values[idx]) + '\n'
                    keys_visited[idx] = True
            file_data += line
    for idx, visited in enumerate(keys_visited):
        if not visited:
            print('Error: key ' + keys[idx] + ' not found')
    with open(params_file, "w") as f:
        f.write(file_data)

def get_qos_status():
    output = shell('slurm-gpu-queue --me')

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
        qos = item.split()[QOS]
        if qos == 'gpu-longlo':
            qos = 'gpu-longlong'
        tres_per_n = item.split()[TRES_PER_N]
        remain_gpu[qos] -= int(tres_per_n.split(':')[-1])
        remain_task[qos] -= 1
    return remain_gpu, remain_task

def config_qos(initial_qos, end_qos):
    qos_time = {
        'gpu-trial'   : '00:20:00',
        'gpu-debug'   : '00:90:00',
        'gpu-short'   : '12:00:00',
        'gpu-normal'  : '30:00:00',
        'gpu-long'    : '3-00:00:00',
        'gpu-longlong': '6-00:00:00'
    }
    qos_list = list(qos_time.keys())
    qos_id = 0
    qos_list = qos_list[qos_list.index(initial_qos):(qos_list.index(end_qos) + 1)]
    if fast_qos is not None:
        qos_list = qos_list + [fast_qos]
    while True:
        qos = qos_list[qos_id]
        remain_gpu, remain_task = get_qos_status()
        if remain_gpu[qos] > 0 and remain_task[qos] > 0:
            qos_to_set = qos
            break
        qos_id += 1
        if qos_id == len(qos_list):
            qos_id = 0
            time.sleep(60)

    if num_gpus == 4:
        partition = 'nv-gpu,nv-gpu-hw'
    elif num_gpus < 4:
        partition = 'nv-gpu'
    elif num_gpus > 4:
        partition = 'nv-gpu-hw'
    else:
        raise Exception('Invalid num_gpus: ' + str(num_gpus))

    file_data = ""
    with open(slurm_file, "r") as f:
        for line in f:
            if line.startswith('#SBATCH --qos='):
                line = '#SBATCH --qos=' + qos_to_set + '\n'
            elif line.startswith('#SBATCH -t'):
                line = '#SBATCH -t ' + qos_time[qos_to_set] + '\n'
            elif line.startswith('#SBATCH -p'):
                line = '#SBATCH -p ' + partition + '\n'
            elif line.startswith('#SBATCH --gres=gpu'):
                line = '#SBATCH --gres=gpu:' + str(num_gpus) + '\n'
            file_data += line
    with open(slurm_file, "w") as f:
        f.write(file_data)

    file_data = ""
    with open(sh_file, "r") as f:
        for line in f:
            if line.startswith('    --nproc_per_node='):
                line = '    --nproc_per_node=' + str(num_gpus) + ' \\\n'
            file_data += line
    with open(sh_file, "w") as f:
        f.write(file_data)

def get_feature_status():
    output = shell('slurm-gpu-info')
    flag = False

    result = {'partition':[], 'features':[], 'name':[], 'remain':[]}
    for item in output.split():
        if 'drain' in item or 'down' in item or 'drng' in item:
            flag = True
        if 'nv-gpu-hw' in item:
            partition = 'nv-gpu-hw'
        elif 'nv-gpu' in item:
            partition = 'nv-gpu'
        elif 'compute-' in item or 'gpu-' in item:
            name = item
        elif 'gpu:' in item and 'IDX:' not in item:
            total = int(item.split(':')[1][0])
        elif 'IDX:' in item:
            used = int(item.split(':')[2][0].split('(')[0])
            remain = total - used
            if remain == 0:
                flag = True
        elif 'IB,' in item:
            features = item.split(',')[3]
            if flag:
                flag = False
                continue
            result['partition'].append(partition)
            result['features'].append(features)
            result['name'].append(name)
            result['remain'].append(remain)
    return result 

def valid_features():
    valid = {'a100': False, 'volta': False, 'rtx8000': False}
    result = get_feature_status()
    for i, f in enumerate(result['features']):
        if 'A100' in f and int(result['remain'][i]) >= num_gpus:
            valid['a100'] = True
        if 'V100' in f and int(result['remain'][i]) >= num_gpus:
            valid['volta'] = True
        if 'RTX' in f and int(result['remain'][i]) >= num_gpus:
            valid['rtx8000'] = True

#    valid_features = ['A100', 'A100|Volta', 'A100|Volta|RTX8000']
    valid_features = ['Volta', 'Volta', 'Volta|RTX8000']
#    if valid['a100']:
#        valid_features = valid_features
    if valid['volta']:
        valid_features = valid_features[1:]
    else:
        valid_features = valid_features[2:]

    return valid_features

def config_feature(feature):
    file_data = ""
    with open(slurm_file, "r") as f:
        for line in f:
            if line.startswith('#SBATCH --constraint='):
                line = '#SBATCH --constraint=' + feature + '\n'
            file_data += line
    with open(slurm_file, "w") as f:
        f.write(file_data)

def get_state_status(check_id):
    output = shell('slurm-gpu-queue --me')
    for item in output.split('\n')[1:]:
        if len(item.split()) < 10:
            continue
        job_id = item.split()[JOBID]
        if job_id == check_id:
            return(item.split()[STATE])
    raise ValueError('job id not found')
    

def main():
    with open(csv_file,'w') as f:
        csv.writer(f).writerow([' ', ' '] + list(params_dict.keys()))

    tuning_list = list(product(*params_dict.values()))
    if use_white_list:
        tuning_list.extend(white_list)

    print(list(params_dict.keys()))
    for idx, values in enumerate(tuning_list):
        if values in block_list: continue
        if values == (): continue
        if idx < start_idx: continue

        print('idx = %d / %d' % (idx, len(tuning_list) - 1))
        for idx, val in enumerate((values)):
            print(str(list(params_dict.keys())[idx]) + ' = ' + str(val))

        config_qos(minimum_qos, maximum_qos)
        config_params(list(params_dict.keys()), values)
        job_id, saved_dir, saved_dir_all_path = submit()
        with open(csv_file,'a') as f:
            csv.writer(f).writerow([job_id, saved_dir] + list(values))
        os.symlink(os.path.abspath('./') + '/' + saved_dir_all_path, link_path + saved_dir)


if __name__ == '__main__':
    main()
