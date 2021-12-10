import random
import socket

msg = [
    'get_task',
    'task_exist',
    'upload_experement',
    'task_error',
    'task_complete'
]
while True:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 8008))
    print('Connected')

    currmsg = msg[random.randint(0, 4)].encode('ascii')
    client_sock.send(currmsg)
    print(f'Sended: {currmsg}')

    data = client_sock.recv(1024)
    print('Received', repr(data))

    client_sock.close()
