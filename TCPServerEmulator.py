import logging
import random
import socket
import time
from threading import Thread
import os

def task_exists():
    pass
def upload_experement():
    pass
def get_task():
    pass
def task_error():
    pass
def task_complete():
    pass

class ThreadedServer(Thread):
    def __init__(self, host, port, timeout=60, debug=logging.DEBUG):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug
        logging.basicConfig(level=self.debug)
        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        logging.debug(f'SERVER Starting...')
        self.listen()

    def listen(self):
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to its host and port
        self.sock.bind((self.host, self.port))
        logging.debug(f'SERVER Socket Bound {self.host} {self.port}')

        # start listening for a client
        self.sock.listen(5)
        logging.debug(f'SERVER Listening...')
        while True:
            # get the client object and address
            client, address = self.sock.accept()

            # set a timeout
            client.settimeout(self.timeout)
            logging.debug(f'CLIENT Listening: {client}')

            # start a thread to listen to the client
            Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        # set a buffer size ( could be 2048 or 4096 / power of 2 )
        size = 1024
        while True:
            try:
                # try to receive data from the client
                data = client.recv(size).decode('ascii')
                if data:
                    data = data.rstrip('\0')
                    logging.debug(f'Data Received {address} \nData:\n{data}')

                    # TODO разработать обработку запросов
                    if data == 'get_task':
                        filename = f'backup{os.sep}FAP38488_8dd91b14_4.fast5'
                        separator = '|'
                        filesize = os.path.getsize(filename)
                        if random.random()>0.5:
                            client.send(f'{filename.split(os.sep)[-1]}{separator}{filesize}'.encode('ascii'))
                            BUFFER_SIZE = 4096
                            logging.debug(f'File send to {address}')
                            with open(filename, "rb") as f:
                                while True:
                                    bytes_read = f.read(BUFFER_SIZE)
                                    if not bytes_read:
                                        break
                                    client.sendall(bytes_read)
                        else:
                            client.send()
                    elif data == 'task_error':
                        pass
                    elif data == 'task_complete':
                        pass
                    elif data == 'upload_experement':
                        pass
                    else:
                        client.send(f'Unknown command {data}'.encode('ascii'))

                    client.close()
                else:
                    raise error('CLIENT Disconnected')
            except:
                logging.debug(f'CLIENT Disconnected: {client}')
                client.close()
                return False


if __name__ == "__main__":
    ThreadedServer('172.31.64.13', 8008, timeout=86400, debug=True).start()
