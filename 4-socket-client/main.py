import socket
import time
from multiprocessing import Process
from typing import Tuple


def split_text(text: str) -> Tuple:
    parts = text.split(':')
    if len(parts) != 2:
        print("ошибка! формат 'имя: сообщение'")
        return None, None,

    f_name = parts[0]
    message = parts[1].lstrip()
    return f_name, message,


def receive(conn: socket):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode('utf-8'))


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 51845
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    name = "John"  # name
    s.send(name.encode('utf-8'))

    t_receive = Process(target=receive, args=(s, ))
    t_receive.start()

    while True:
        # ask the client whether he wants to continue
        text = input(':')

        if text == 'q':
            break

        friend_name, _ = split_text(text)
        if friend_name is None:
            continue

        if friend_name != name and t_receive.is_alive():
            s.send(text.encode('utf-8'))
            # print(f"{name}->{text}")
        else:
            continue

    if t_receive.is_alive():
        t_receive.terminate()

    s.close()
