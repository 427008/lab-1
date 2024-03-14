import socket
import sys
from math import sqrt


def create_server() -> socket:
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 0, ))
        server.listen(1)
    except OSError as msg:
        print(msg)
        sys.exit(1)

    if server is None:
        print('could not open server socket')
        sys.exit(1)

    return server

def run_server_connection(server: socket) -> None:
    print('Wait...')
    conn, addr = server.accept()
    with conn:
        print('Connected by', addr)
        file = open("hello.html", "r")
        hello = file.read()
        data = hello.encode('utf-8')
        conn.send(data)
        while True:
            r = conn.recv(1024)
            if r.decode('utf-8') == 'stop':
                break
            conn.send(data)
