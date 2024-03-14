import socket
# from _thread import *
from threading import Thread, Lock
from TcpServer import run_server_connection, create_server, loop

lock = Lock()
clients = {}


def threaded(conn: socket, sender: str):
    while True:
        _data = conn.recv(1024)
        if not _data:
            break

        # reverse the given string from client
        data_str = _data.decode('utf-8')
        print('get', data_str)
        if data_str == 'q':
            break

        parts = data_str.split(':')
        if len(parts) != 2:
            message = f"ошибка, формат 'имя: сообщение'"
            conn.send(message.encode('utf-8'))
            print('post back', message)
            continue

        friend_name = parts[0]
        message = parts[1].lstrip()

        if friend_name not in clients.keys():
            message = f"server: ошибка, имя '{friend_name}' не найдено"
            conn.send(message.encode('utf-8'))
            print('post back', message)
            continue

        message = f"{sender}: {message}"
        friend_conn = clients[friend_name]
        if friend_conn.fileno() == -1:
            message = f"server: ошибка, '{friend_name}' ушел"
            conn.send(message.encode('utf-8'))
            print('post back', message)
            continue

        friend_conn.send(message.encode('utf-8'))
        print('post', message)

    # connection closed
    conn.close()


if __name__ == '__main__':
    server = create_server()
    laddr = server.getsockname()
    print('running on ', laddr)
    port = laddr[1]

    threads = []
    while True:
        # establish connection with client
        conn, addr = server.accept()
        print('Connected to :', addr[0], ':', addr[1])

        data = conn.recv(1024)
        name = data.decode('utf-8')
        if name in clients.values():
            data = f"'{name}' уже тут, вы не '{name}'".encode('utf-8')
            conn.send(data)
            conn.close()
            continue

        for _, friend in clients.items():
            data = f"server: пришел '{name}'".encode('utf-8')
            friend.send(data)

        with lock:
            clients[name] = conn

        t = Thread(target=threaded, args=(conn, name, ))
        t.start()
        threads.append(t)
        # TODO replace threading with multiprocessing
        # Thread has no result, cannot be terminated

    # server.close()
    # print(f"Quit")
