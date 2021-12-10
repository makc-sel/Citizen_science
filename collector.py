import os
import random
from glob import glob
from shutil import copyfile, rmtree

path_to_process_dir = './process/'
path_to_result_dir = './result/'

if os.path.exists(path_to_process_dir):
    dirs = glob(path_to_process_dir + '*')
    if len(dirs) > 0:
        for dir in dirs:
            if os.path.exists(dir + '/result.zip'):
                if not os.path.exists(path_to_result_dir):
                    os.mkdir(path_to_result_dir)
                copyfile(dir + '/result.zip', path_to_result_dir + f'{random.randint(0, 10)}result.zip')
                rmtree(dir)
            print(dir)
else:
    print('Папки process ненайдено!')
