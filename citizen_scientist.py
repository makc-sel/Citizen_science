import atexit
import configparser
import datetime
import os
import time
from glob import glob
from zipfile import ZipFile, ZIP_DEFLATED

import pause


def zipdir(path, ziph):
    for file in glob(path + '*'):
        print(file)
        if 'fast5' in file or 'flag' in file:
            ziph.write(file)


def on_exit(dir):
    if DEBUG:
        print(f'Остановка программы в папке {dir}')
    if os.path.exists(f'{dir}/working.flag'):
        os.remove(f'{dir}/working.flag')
        if DEBUG:
            print(f'working.flag удален')


config = configparser.ConfigParser()
config.read("process.cfg")

DEBUG = bool(config.get('CONFIG', 'debug'))
START_TIME = config.get('WORK_TIME', 'start')
STOP_TIME = config.get('WORK_TIME', 'stop')
ARGUMENTS = config.get('CONFIG', 'arguments')
PATH_TO_GUPPY = config.get('CONFIG', 'path_to_guppy')
DEVICE = config.get('CONFIG', 'device')
path_to_process_dir = './process/'

while True:
    # Получение текущего времени
    start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.strptime(START_TIME, '%H:%M:%S').time())
    stop_time = datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.strptime(STOP_TIME, '%H:%M:%S').time())
    curr_time = datetime.datetime.now()

    if start_time < curr_time and stop_time > curr_time:
        if DEBUG:
            print('Начало работы', curr_time)
        if os.path.exists(path_to_process_dir):
            for dir in glob(path_to_process_dir + '*'):
                atexit.register(on_exit, dir)
                if DEBUG:
                    print(f'Проверяем папку {dir}', end=' ')
                if os.path.exists(dir + '/start.flag') and not os.path.exists(dir + '/working.flag') and not os.path.exists(dir + '/finish.flag'):
                    try:
                        open(dir + '/working.flag', 'x').close()
                    except FileExistsError:
                        if DEBUG:
                            print('в данной папке ведетется работа.')
                        continue
                    if DEBUG:
                        print(f'Запуск guppy в {dir}')

                    # Запуск guppy_basecaller
                    os.system(rf'"{PATH_TO_GUPPY}" -i {dir} -s {dir} --device {DEVICE} {ARGUMENTS}')

                    # Удаление fast5 файла
                    for fast5 in glob(dir + '*.fast5'):
                        os.remove(fast5)
                    if DEBUG:
                        print('Файл fast5 удален')

                    # Архивация файлов
                    zipf = ZipFile(dir + '/result.zip', 'w', ZIP_DEFLATED)
                    zipdir(dir, zipf)
                    zipf.close()
                    if DEBUG:
                        print('Файлы заархивированы')

                    # Создание флага окончания работы
                    open(dir + '/finish.flag', 'x').close()
                    if DEBUG:
                        print('Guppy закончил работу!')
                else:
                    if DEBUG:
                        print('')
                atexit.unregister(on_exit)
            time.sleep(5)
        else:
            if DEBUG:
                print('no job')
            time.sleep(5)
    else:
        if stop_time < curr_time:
            pause_time = start_time + datetime.timedelta(days=1)
            if DEBUG:
                print('Рабочее время закончено, ждем до', pause_time)
            pause.until(pause_time)
        elif start_time > curr_time:
            if DEBUG:
                print('Рабочее время не началось, ждем до', start_time)
            pause.until(start_time)
