import os
import sys
import time
import numpy as np
from itertools import product
import params
import csv

'''
Need to config:
params_dict: the dict to config the params
slurm_file: the file to submit the job
params_file: the file to config the params
params_indent: the indent of the params in params_file
csv_file: the file to save the results
'''

params_dict = {}
params_dict.update({'transformer.enc_pf_dim': [512, 1024]})
params_dict.update({'transformer.dropout': [0., 0.1]})

block_list = [
    (),
    (),
]

white_list = [
    (),
    (),
]

use_white_list = True

#block_dict = {}
#for keys in params_dict:
#    block_dict.update({keys: []})

slurm_file = './run_IO_vae.slurm'
params_file = './params.py'
params_indent = ' ' * 4
new_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
csv_file = 'log.tuning_csvs/tuning_IO_vae_' + new_time + '.csv'

def submit():
    process = os.popen('sbatch ' + slurm_file)
    output = process.read()
    process.close()
    print(output)
    job_id = output.split()[-1]
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
    while True:
        time.sleep(1)
        new_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        if new_time != old_time:
            break
    return job_id, saved_dir, saved_dir_all_path

def config_params(keys, values):
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

def main():
    with open(csv_file,'w') as f:
        csv.writer(f).writerow([' ', ' '] + list(params_dict.keys()))

    tuning_list = list(product(*params_dict.values()))
    if use_white_list:
        tuning_list.extend(white_list)

    print(list(params_dict.keys()))
    for values in tuning_list:
        if values in block_list: continue
        if values == (): continue

        for idx, val in enumerate((values)):
            print(str(params_dict.keys()[idx]) + ' = ' + str(val))

        config_params(list(params_dict.keys()), values)
        job_id, saved_dir, saved_dir_all_path = submit()
        with open(csv_file,'a') as f:
            csv.writer(f).writerow([job_id, saved_dir] + list(values))
        os.symlink(os.path.abspath('./') + '/' + saved_dir_all_path, './trained_models/tuning/' + saved_dir)


if __name__ == '__main__':
    main()