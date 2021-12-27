import os
from glob import glob


path_to_source_dir = './source/'
path_to_process_dir = './process/'

files = glob(path_to_source_dir + '*.fast5')
tmp_dirs = glob(path_to_process_dir + '*')
count_files = len(files)
# tmp.split('_')[-1]
i = 0
for file in files:
    if os.path.exists(f'{path_to_process_dir}tmp_{i}'):
        print('exist')
    i += 1

# for tmp in tmp_dirs:
#     print(tmp.split('_')[-1])

# umnovaolga15@gmail.com
# https://community.nanoporetech.com/downloads
# guppy_basecaller -i test -s guppy_results --flowcell FLO-MIN107 --kit SQK-RNA002
# guppy_basecaller -i test -s guppy_results --flowcell FLO-MIN107 --kit SQK-RNA002 --device cuda:0