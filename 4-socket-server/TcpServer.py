import socket
import sys
import time
from threading import Lock
from typing import List, Dict


def create_server() -> socket:
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 0,))
        server.listen(4)
    except OSError as msg:
        print(msg)
        sys.exit(1)

    if server is None:
        print('could not open server socket')
        sys.exit(1)

    return server


def run_server_connection(server: socket, clients: Dict, lock: Lock) -> None:
    conn, _ = server.accept()
    with (conn):
        data = conn.recv(1024)
        name = data.decode('utf-8')
        if name in clients.values():
            data = f"'{name}' уже тут, вы не '{name}'".encode('utf-8')
            conn.send(data)
            return

        for _, friend in clients.items():
            data = f"server: пришел '{name}'".encode('utf-8')
            friend.send(data)

        with lock:
            clients[name] = conn


def loop(clients: Dict, lock: Lock):
    while True:
        for name, conn in clients.items():
            print('loop', name)
            # data = f"server: пришел '{name}'".encode('utf-8')
            # friend.send(data)
            pass
        time.sleep(1)

    # while True:
    #     data = conn.recv(1024)
    #     message = data.decode('utf-8')
    #     print('get', message)
    #     if message == 'q':
    #         break
    #
    #     parts = message.split(':')
    #     if len(parts) != 2:
    #         message = f"ошибка, формат 'имя: сообщение'"
    #         data = message.encode('utf-8')
    #         conn.send(data)
    #         print('post', message)
    #         continue
    #
    #     friend_name = parts[0]
    #     message = parts[1].lstrip()
    #
    #     if friend_name not in clients.keys():
    #         message = f"ошибка, имя: '{friend_name}' не найдено"
    #         data = message.encode('utf-8')
    #         conn.send(data)
    #         print('post', message)
    #         continue
    #
    #     friend = clients[friend_name]
    #     message = f"{name}: {message}"
    #     data = message.encode('utf-8')
    #     friend.send(data)
    #     print('post', message)
