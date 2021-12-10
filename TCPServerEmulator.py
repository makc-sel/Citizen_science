import logging
import random
import socket
import time
from threading import Thread


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
                    logging.debug(f'Data Received {client} {address} \nData:\n{data}')

                    # TODO разработать обработку запросов
                    time.sleep(random.random())

                    # send a response back to the client
                    response = data
                    client.send(response.encode('ascii'))
                else:
                    raise error('CLIENT Disconnected')
            except:
                logging.debug(f'CLIENT Disconnected: {client}')
                client.close()
                return False


if __name__ == "__main__":
    ThreadedServer('127.0.0.1', 8008, timeout=86400, debug=True).start()
