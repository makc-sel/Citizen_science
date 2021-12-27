import configparser
import datetime
import logging
import socket
import time
import os
import pause
import atexit
from pathlib import Path
from shutil import make_archive, rmtree


def on_exit():
    logging.debug(f'Остановка программы')


path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "process.cfg")

config = configparser.ConfigParser()
config.read(config_path)

DEBUG = bool(config.get('CONFIG', 'debug'))
START_TIME = config.get('WORK_TIME', 'start')
STOP_TIME = config.get('WORK_TIME', 'stop')
ARGUMENTS = config.get('CONFIG', 'arguments')
PATH_TO_GUPPY = config.get('CONFIG', 'path_to_guppy').lstrip()
if ' ' in PATH_TO_GUPPY:
    PATH_TO_GUPPY = f'"{PATH_TO_GUPPY}"'

DEVICE = config.get('CONFIG', 'device')
path_to_process_dir = './process/'
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

SERVER = '172.31.64.13'
PORT = 8008

while True:
    # Получение текущего времени
    logging.debug(f'Получение текущего времени')
    start_time = datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.strptime(START_TIME, '%H:%M:%S').time())
    stop_time = datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.strptime(STOP_TIME, '%H:%M:%S').time())
    curr_time = datetime.datetime.now()

    if start_time < curr_time and stop_time > curr_time:
        logging.debug(f'Начало работы {curr_time}')

        # TODO Реализация запросов к серверу и обработка ответа обработка ошибок
        # Ошибка подключения / Сервер не отвечает / Нет соединения с интернетом (сервером)
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((SERVER, PORT))
        logging.debug(f'Подключен к {SERVER}')

        msg = 'get_task'.encode('ascii')
        client_sock.send(msg)
        logging.debug(f'Отослано на {SERVER}: {msg}')

        data = client_sock.recv(512).decode('ascii')
        logging.debug(f'Получено от {SERVER}: {data}')

        if data:
            BUFFER_SIZE = 4096
            filename, filesize = data.split('|')
            filesize = int(filesize)
            path_to_folder = os.path.join(ROOT_DIR, filename.split('.')[0])
            path_to_file = os.path.join(path_to_folder, filename)
            path_to_result = os.path.join(ROOT_DIR, f"{filename.split('.')[0]}_result")

            # Создание папки для файла
            try:
                os.makedirs(filename.split('.')[0])
            except FileExistsError:
                pass

            # Нехватка памяти / Ошибка загрузки / Разрыв связи
            logging.debug(f'Загрузка задачи из {SERVER}')
            if os.path.exists:
                logging.debug(os.path.getsize(path_to_file)==filesize)

            with open(path_to_file, "wb") as f:
                while True:
                    bytes_read = client_sock.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)

            # Запуск guppy_basecaller
            # Ошибки: ошибки с гуппи, нехватка мощности и тд
            logging.debug(f'Guppy закончил работу в папке {path_to_folder}')
            result = os.system(rf'{PATH_TO_GUPPY} -i {path_to_folder} -s {path_to_result} --device {DEVICE} {ARGUMENTS}')
            if result == 0:
                logging.debug(f'Guppy закончил работу результат в папке {path_to_result}')
            else:
                logging.debug(f'Guppy закончил работу с ошибкой')

            # Сжатие результата
            make_archive(path_to_result, 'zip', path_to_result)
            logging.debug(f'Результат сжат')

            # Отправка результата на сервер

        else:
            logging.debug(f'No task {SERVER}')
        client_sock.close()
        time.sleep(10)

    else:
        if stop_time < curr_time:
            pause_time = start_time + datetime.timedelta(days=1)
            logging.debug(f'Рабочее время закончено, ждем до {pause_time}')
            pause.until(pause_time)
        elif start_time > curr_time:
            logging.debug(f'Рабочее время не началось, ждем до {start_time}')
            pause.until(start_time)
